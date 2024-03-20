from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
import pandas as pd
import cv2
import pytesseract
import time
import base64
import json
import numpy as np
from selenium.webdriver.common.by import By
from multiprocessing import Pool
from collections import ChainMap


op = webdriver.ChromeOptions()
# op.add_argument('headless')
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
op.add_experimental_option('prefs', prefs)
op.add_argument('--kiosk-printing')
op.add_argument('--headless')
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-shm-usage')
# pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'


def main():
    data_pd = pd.read_csv('finaladmitcarddetailsoffline.csv')
    print(data_pd.columns)
    allData = []
    errorData = []
    process = Pool(12)
    res = process.map(insertDetails, data_pd.to_numpy())
    process.close()
    process.join()


def insertDetails(data):
    tryNum = 0
    driver = webdriver.Chrome("/usr/bin/chromedriver", options=op)
    while (tryNum < 5):
        try:
            path = "https://ntaresults.nic.in/resultservices/JEEMAINauth22s2p1"
            driver.get(path)
            time.sleep(2)
            dob = data[3].split('-')
            # dob = data['DOB'].split('-')
            dayTxt = dob[0]
            monthTxt = dob[1]
            yearTxt = dob[2]
            applicationNumTxt = str(int(data[2]))
            # examSession = Select(driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlExamSession'))
            # examSession.select_by_value('04')  # 01: Feb  02:March  03:April
            driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_txtRegNo').send_keys(applicationNumTxt)
            day = Select(driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlday'))
            day.select_by_value(dayTxt)
            month = Select(driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlmonth'))
            month.select_by_value(monthTxt)
            year = Select(driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlyear'))
            year.select_by_value(yearTxt)

            # captchaImg = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_captchaimg')
            captchaInput = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_Secpin')
            submit = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_Submit1')

            driver.set_window_size(1920, 1080)
            driver.save_screenshot(r'./screenshot.png')
            img = cv2.imread(r"./screenshot.png")
      
            y = 395
            x = 920

            h = 45
            w = 100
            img = img[y:y + h, x:x + w]


            img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1, 1), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)


            cv2.imwrite(r"./capimg.png", img)
            captchaTxt = pytesseract.image_to_string(img).split('\n')[0].split(' ')[0]
            print(captchaTxt)
            captchaInput.send_keys(captchaTxt)
            try:
                submit.click()
                time
                .sleep(1)
                driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_pnlcandinfo')
                result = retrieveDetails(driver, applicationNumTxt)
                pd.DataFrame([result]).to_csv("successresultdatajeemainsoffline.csv", mode='a', header=False, encoding='utf-8', index=None)
                return data
            except UnexpectedAlertPresentException as e:
                tryNum = tryNum + 1
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    continue
                break
        except Exception as e:
            tryNum = tryNum + 1
            print('Some Error Occured, Trying Again, Exception:', e)
    if (tryNum >= 5):
        pd.DataFrame([data]).to_csv("failedresultdatajeemainsoffline.csv", mode='a', header=False, encoding='utf-8', index=None)
        return {"error": True}
    return


def retrieveDetails(driver, applicationNumTxt):

    time.sleep(1)

    rollNoSession1 = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_rollno_Jan').text
    rollNoSession2 = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_rollno_apr').text


    name = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_cname').text

    fathername = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_fname').text
    mothername = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_mname').text

    category = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_cat').text
    pwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_pwd').text

    gender = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_gender').text
    dob = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_dob').text

    state = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_scode_e').text
    nationality = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_nation').text

    sess1Phy = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_PHY_P1A').text
    sess1Chem = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_CHE_P1A').text
    sess1Math = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_MAT_P1A').text

    sess2Phy = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_PHY_P1B').text
    sess2Chem = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_CHE_P1B').text
    sess2Math = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_MAT_P1B').text

    totalPhy = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_PHY_P1F').text
    totalChem = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_CHE_P1F').text
    totalMath = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_MAT_P1F').text

    sess1Total = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_TOT_P1A').text
    sess2Total = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_TOT_P1B').text

    finalTotal = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_PS_TOT_P1F').text
    finalInWord = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_MRK_FIG1').text

    airCrl = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_crl1').text
    airGenEws = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_ews1').text
    airObcNcl = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_obc1').text
    airSc = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_sc1').text
    airSt = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_st1').text
    airCrlPwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_crl1ph').text
    airGenEwsPwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_ews1ph').text
    airObcNclPwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_obc1ph').text
    airScPwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_sc1ph').text
    airStPwd = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ai_st1ph').text

    try:
        profilePic = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_imgprvw')
        base64ProfileImg = profilePic.get_attribute('src')

        img = base64.b64decode(base64ProfileImg.split(',')[1])
        with open("photos/" + str(applicationNumTxt) + '_pic.png', "wb") as fh:
            fh.write((img))
    except:
        pass

    driver.set_window_size(1920, 1080)
    driver.save_screenshot('result/Application_Number_SC' + str(applicationNumTxt) + '.png')
    driver.close()
    driver.quit()

    return {
        "applicationNumTxt": applicationNumTxt,
        "name": name,
        "fatherName": fathername,
        "motherName": mothername,
        "category": category,
        "pwd": pwd,
        "gender": gender,
        "dob": dob,
        "state": state,
        "nationality": nationality,
        "RollNumberSession1": rollNoSession1,
        "RollNumberSession2": rollNoSession2,

        "Session1-Physics": sess1Phy,
        "Session1-Chemistry": sess1Chem,
        "Session1-Maths": sess1Math,
        "Session1-Total": sess1Total,

        "Session2-Physics": sess2Phy,
        "Session2-Chemistry": sess2Chem,
        "Session2-Maths": sess2Math,
        "Session2-Total": sess2Total,

        "Total-Physics": totalPhy,
        "Total-Chemistry": totalChem,
        "Total-Maths": totalMath,

        "Final Total": finalTotal,
        "Final In Words": finalInWord,
      
        "AIR-CRL": airCrl,
        "AIR-GEN-EWS": airGenEws,
        "AIR-OBC-NCL": airObcNcl,
        "AIR-SC": airSc,
        "AIR-ST": airSt,
        "AIR-CRL-PwD": airCrlPwd,
        "AIR-GEN-EWS-PwD": airGenEwsPwd,
        "AIR-OBC-NCL-PwD": airObcNclPwd,
        "AIR-SC-PwD": airScPwd,
        "AIR-ST-PwD": airStPwd,

    }


if __name__ == '__main__':
    d = main()
