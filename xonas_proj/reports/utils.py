from dotenv import load_dotenv
import os


load_dotenv()

REPORT_URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod?'

token_dict = {
    'Kochergin': os.getenv('WB_CAB_TOKEN_KOCHER'),
    'Tishka': os.getenv('WB_CAB_TOKEN_TISHKA'),
    'Hanisenko': os.getenv('WB_CAB_TOKEN_HANISENKO'),
    'Dementeva': os.getenv('WB_CAB_TOKEN_DEMENTEVA'),
    'Shershunov': os.getenv('WB_CAB_TOKEN_SHERSHUNOV'),
    'Kolmikov': os.getenv('WB_CAB_TOKEN_KOLMIKOV'),
    'Kalinin': os.getenv('WB_CAB_TOKEN_KALININ'),
    'Yurtaikina': os.getenv('WB_CAB_TOKEN_YURTAIKINA'),
    'Grachev': os.getenv('WB_CAB_TOKEN_GRACHEV'),
    'Beloglintsev': os.getenv('WB_CAB_TOKEN_BELOGLINTSEV'),
    'Ageeva': os.getenv('WB_CAB_TOKEN_AGEEVA'),
    'Skotnikova': os.getenv('WB_CAB_TOKEN_SKOTNIKOVA'),
    'Galibin': os.getenv('WB_CAB_TOKEN_GALIBIN'),
    'Ignatovich': os.getenv('WB_CAB_TOKEN_IGNATOVICH'),
}
