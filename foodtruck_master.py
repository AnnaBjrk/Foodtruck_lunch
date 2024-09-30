import requests
import re
import easyocr


from bs4 import BeautifulSoup


def reads_page_and_creates_a_list_of_all_image_urls() -> list:
    url = "https://www.sthlmstreetlunch.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    print(response)

    soup = BeautifulSoup(response.content, "html.parser")
    image_bank = []
    for image_code in soup.find_all(class_="sqs-image-shape-container-element"):
        # image_code = soup.find(class_="sqs-image-shape-container-element")
        image_code = str(image_code)
        image_code = image_code.replace("\n", "")
        image_code = image_code.replace('"', "")

        image_code = re.sub(r"<div class.*?srcset=", "",
                            image_code, flags=re.IGNORECASE)
        image_code = re.sub(r"=100w.*$", "", image_code, flags=re.IGNORECASE)
        image_bank.append(image_code)
    return image_bank


def validate_content_in_image(url: str) -> bool:
    '''returns true if an image includes the words Campus Solna or Svartz'''
    reader = easyocr.Reader(['en'])
    # result = reader.readtext(
    # "https://images.squarespace-cdn.com/content/v1/5705576e4d088ef8415fc3e2/7c96acc3-2dd5-4b64-848b-92bf84cfbfc5/3.png?format=750w")
    result = reader.readtext(url)
    for detection in result:
        check = (detection[1])
        check = str(check)
        check = check.replace("\n", "")
        check = check.lower()
        print(check)
        if "solna" in check:
            print("yessss")
            return True
    return False


def main():

    # finds the image with solna in it.
    image_urls = reads_page_and_creates_a_list_of_all_image_urls()
    print(image_urls)
    for image_link in image_urls:
        if validate_content_in_image(image_link):
            solna_lunch_image_link = image_link
            break

        print(solna_lunch_image_link)


if __name__ == "__main__":
    main()
