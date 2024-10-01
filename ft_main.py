import requests
import re
import easyocr
# import BeautifulSoup


from bs4 import BeautifulSoup


def reads_page_and_creates_a_list_of_all_image_urls() -> list:
    '''a function that reads through the page
    Returns : a list with links to all images on the page'''
    url = "https://www.sthlmstreetlunch.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    all_images = []
    for image_code in soup.find_all(class_="sqs-image-shape-container-element"):
        # This is the class in the code where the images are stored
        image_code = str(image_code)
        image_code = image_code.replace("\n", "")
        image_code = image_code.replace('"', "")
        # With regex the long string of code from the web is striped of all code exept the one for the image link.
        # There are several image links in the code string referring to the same image only one is choosen
        image_code = re.sub(r"<div class.*?srcset=", "",
                            image_code, flags=re.IGNORECASE)
        image_code = re.sub(r"=100w.*$", "", image_code, flags=re.IGNORECASE)
        all_images.append(image_code)
    return all_images


def validate_content_in_image(url: str) -> bool:
    ''' Extracts the text from each image in the list with image links, using easyocr package. Checks if the image contains the word Solna
    Input variable a url to an image.
    Returns true if an image includes the word Solna. False if it doesent'''
    reader = easyocr.Reader(['en'])
    result = reader.readtext(url)
    for detection in result:
        check = (detection[1])
        check = str(check)
        check = check.replace("\n", "")
        check = check.lower()
        if "solna" in check:
            return True
    return False


def main():
    '''This program is about fetching info about what foodtrucks are parking at Solna Campus each week.
    The program calls two functions one that fetches links to all images on the https://www.sthlmstreetlunch.com webpage 
    and one that reads through the images looking for the word Solna.
    If an image with Solna is found - the program prints it out.'''

    # creates a list with urls to the images on the page
    image_urls = reads_page_and_creates_a_list_of_all_image_urls()
    found = False
    for image_link in image_urls:  # finds the image with solna in it.
        if validate_content_in_image(image_link):
            solna_lunch_image_link = image_link
            print("\n***************************************")
            print("\nThe list with the food trucks for the week, has been fetched. ")
            print(solna_lunch_image_link)
            found = True
            break
    if found == False:
        print("\n***************************************")
        print("\nIngen info om food trucks i Solna hittades tyvärr")


if __name__ == "__main__":
    main()
