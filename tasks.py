from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from robocorp import browser
import shutil
@task
def order_robot():
    browser.configure(
        slowmo=100,
    )
    open_robot_order()
    download_order_file()
    fill_form_with_csv_file()
    archive_receipt()
    clean_up_folders()
def open_robot_order():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page=browser.page()
    page.click("text=OK")
def download_order_file():
    http=HTTP()
    http.download(
        url="https://robotsparebinindustries.com/orders.csv",
        target_file="orders.csv",
        overwrite=True
    )
def fill_form_with_csv_file():
    tables=Tables()
    order_table=tables.read_table_from_csv("orders.csv")
    for order in order_table:
        fill_order_form(order)
def fill_order_form(order):
    page=browser.page()
    head_names={
        "1":"Roll-a-thor head",
        "2":"Peanut crusher head",
        "3":"D.A.V.E head",
        "4":"Andy Roid head",
        "5":"Spanner mate head",
        "6":"Drillbit 2000 head",
    }
    head_numbers=order["Head"]
    page.select_option("#head",head_names.get(head_numbers))
    page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(order["Body"]))
    page.fill("input[placeholder='Enter the part number for the legs']",order["Legs"])
    page.fill('#address',order["Address"])
    while True:
        page.click('#order')
        another_order=page.query_selector("#order-another")
        if another_order:
            pdf_file_path = store_receipt_as_pdf(int(order["Order number"]))
            screenshot_file_path=store_receipt_as_screenshot(int(order["Order number"]))
            assembled_screenshot_as_receipt(screenshot_file_path,pdf_file_path)
            another_order_robot()
            close_annoying_model()
            break
def store_receipt_as_pdf(order_number):
    page=browser.page()
    order_receipt=page.locator("#receipt").inner_html()
    pdf=PDF()
    pdf_file_path=f"output/receipt/{order_number}.pdf"
    pdf.html_to_pdf(order_receipt,pdf_file_path)
    return pdf_file_path
def store_receipt_as_screenshot(order_number):
    page=browser.page()
    screenshot_path=f"output/screenshot/{order_number}.png"
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path
def assembled_screenshot_as_receipt(screenshot_path,pdf_file_path):
    pdf=PDF()
    pdf.add_watermark_image_to_pdf(image_path=screenshot_path,source_path=pdf_file_path,output_path=pdf_file_path)
def another_order_robot():
    page=browser.page()
    page.click("#order-another")
def close_annoying_model():
    page=browser.page()
    page.click("text=OK")
def archive_receipt():
    zip_folder=Archive()
    zip_folder.archive_folder_with_zip("output/receipt","output/receipt.zip")
def clean_up_folders():
    shutil.rmtree("output/receipt")
    shutil.rmtree("output/screenshot")
































# from robocorp.tasks import task
# from robocorp import browser
# from RPA.HTTP import HTTP
# from RPA.Tables import Tables
# from RPA.PDF import PDF
# from RPA.Archive import Archive
# import shutil

# @task
# def order_robots_from_RobotSpareBin():
#     """
#     Orders robots from RobotSpareBin Industries Inc.
#     Saves the order HTML receipt as a PDF file.
#     Saves the screenshot of the ordered robot.
#     Embeds the screenshot of the robot to the PDF receipt.
#     Creates ZIP archive of the receipts and the images.
#     """
#     browser.configure(
#         slowmo=100,
#     )
#     open_robot_order_website()
    
#     orders = get_orders()
#     process_orders(orders)
#     archive_receipt()
#     clean_up_folders()

# def open_robot_order_website():
#     browser.goto("https://robotsparebinindustries.com/#/robot-order")
    

# def get_orders():
#     http = HTTP()
#     http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
#     table = Tables()
#     orders = table.read_table_from_csv("orders.csv")
#     return orders

# def close_annoying_modal():
#     page = browser.page()
#     page.click("text=OK")

# def fill_order_form(order):
#     page=browser.page()
#     head_names={
#         "1":"Roll-a-thor head",
#         "2":"Peanut crusher head",
#         "3":"D.A.V.E head",
#         "4":"Andy Roid head",
#         "5":"Spanner mate head",
#         "6":"Drillbit 2000 head",
#     }
#     head_numbers=order["Head"]
#     page.select_option("#head",head_names.get(head_numbers))
#     page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(order["Body"]))
#     page.fill("input[placeholder='Enter the part number for the legs']",order["Legs"])
#     page.fill('#address',order["Address"])
#     while True:
#         page.click('#order')
#         another_order=page.query_selector("#order-another")
#         if another_order:
#             pdf_file_path = store_receipt_as_pdf(int(order["Order number"]))
#             screenshot_file_path=store_receipt_as_screenshot(int(order["Order number"]))
#             assembled_screenshot_as_receipt(screenshot_file_path,pdf_file_path)
#             another_order_robot()
#             # Remove the following line to keep modal open for next order
#             # close_annoying_modal()
#             break


# def process_orders(orders):
#     for order in orders:
#         close_annoying_modal()
#         fill_order_form(order)
        

# def store_receipt_as_pdf(order_number):
#     page=browser.page()
#     order_receipt=page.locator("#receipt").inner_html()
#     pdf=PDF()
#     pdf_file_path=f"output/receipt/{order_number}.pdf"
#     pdf.html_to_pdf(order_receipt,pdf_file_path)
#     return pdf_file_path


# def store_receipt_as_screenshot(order_number):
#     page=browser.page()
#     screenshot_path=f"output/screenshot/{order_number}.png"
#     page.locator("#robot-preview-image").screenshot(path=screenshot_path)
#     return screenshot_path


# def assembled_screenshot_as_receipt(screenshot_path,pdf_file_path):
#     pdf=PDF()
#     pdf.add_watermark_image_to_pdf(image_path=screenshot_path,source_path=pdf_file_path,output_path=pdf_file_path)


# def another_order_robot():
#     page=browser.page()
#     page.click("#order-another")
#     close_annoying_modal()
    
    
# def archive_receipt():
#     zip_folder=Archive()
#     zip_folder.archive_folder_with_zip("output/receipt","output/receipt.zip")
    
    
# def clean_up_folders():
#     shutil.rmtree("output/receipt")
#     shutil.rmtree("output/screenshot")
