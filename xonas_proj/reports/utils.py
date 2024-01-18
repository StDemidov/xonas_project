from dotenv import load_dotenv
import os


load_dotenv()

REPORT_URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod?'

token_dict = {
    'Kochergin': os.getenv('WB_CAB_TOKEN_KOCHER'),
    'Tishka': os.getenv('WB_CAB_TOKEN_TISHKA')
}
