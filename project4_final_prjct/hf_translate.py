from dbwriter import dbsession
import logging
import os
import logging
import re
from googletrans import Translator


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# console logger
logger = logging.getLogger()
dbsession_inst = dbsession("host='52.35.199.96' port=5432 user='healthyfood' password='Y24977c1' dbname='healthyfoodbd'")


def analize_tab(p_table):
    recid = dbsession_inst.select(f'SELECT * from {p_table} limit 1;')
    #logger.debug(f'recid {recid}')
    logger.debug(f'analize table <{p_table}>')
    translator = Translator()
    for n in recid:
        l = len(n)
        for i in range(l):
            logger.debug(f'n{i} <{n[i]}>')
        break

# def translate(p_table, p_keyposition, p_labelposition, p_languagesrc='ru', p_languagedest='en'):
def translate(p_table, p_keyposition, p_labelposition, p_languagesrc='en', p_languagedest='ru'):	
    recid = dbsession_inst.select(f"SELECT * from {p_table} where table_source = 'website_text_attributs';")
    #print(f'recid {recid}')
    translator = Translator()
    for n in recid:
        # l = len(n)
        # for i in range(l):
        #     logger.debug(f'n{i} <{n[i]}>')
        exists_check = dbsession_inst.select(f"SELECT count(*) from item_translations \
        	where item_uid = '{n[p_keyposition]}' and language_code in ('{p_languagedest}');")
        if 0 != exists_check[0][0]:
            logger.debug(f'n[p_keyposition] {n[p_keyposition]} already translated on {exists_check[0][0]} language')
            continue
        logger.debug(f'check1 <{exists_check[0][0]}>')
        # break

        det = translator.detect(n[p_labelposition])
        tra = translator.translate(src=p_languagesrc, dest=p_languagedest, text=n[p_labelposition])
        if det.lang!=p_languagesrc:
            logger.debug(f'p_languagesrc <{p_languagesrc}> but det-lang <{det.lang}> for <{n[p_labelposition]}>')
            logger.debug(f'det {det} tra {tra}')
        # logger.debug(f'det-lang {det.lang} det-confidence{det.confidence} ')
        # logger.debug(f'tra-src {tra.src} tra-dest {tra.dest} tra-text {tra.text} tra-pronunciation {tra.pronunciation} tra-extra_data {tra.extra_data} ')
        # break
       
        dbsession_inst.executesql(
            "insert into item_translations (item_uid, language_code, translation, table_source) values ('{}','{}','{}','{}');" \
            .format(n[p_keyposition], p_languagedest, tra.text.replace('\'', '\'\''),"website_text_attributs"))
        
        # dbsession_inst.executesql(
        #     "insert into item_translations (item_uid, language_code, translation,table_source) values ('{}','{}','{}','{}');" \
        #     .format(n[p_keyposition], p_languagesrc, n[2].replace('\'', '\'\''),p_table))
        dbsession_inst.executesql('commit;')


# def translate():
#     recid = dbsession_inst.select('SELECT * from recepies_instructions_cpy;')
#     print(f'recid {recid}')
#     translator = Translator()
#     for n in recid:
#         print(f'n 0<{n[0]}> 1<{n[1]}> 2<{n[2]}> 3<{n[3]}>')
#         det = translator.detect(n[2])
#         tra = translator.translate(n[2])
#         print(f'det {det} tra {tra}')
#         # print(f'det-lang {det.lang} det-confidence{det.confidence} ')
#         # print(f'tra-src {tra.src} tra-dest {tra.dest} tra-text {tra.text} tra-pronunciation {tra.pronunciation} tra-extra_data {tra.extra_data} ')
#         dbsession_inst.executesql("insert into item_translations (item_uid, language_code, translation) values ('{}','{}','{}');" \
#                                 .format(n[4], tra.dest, tra.text.replace('\'', '\'\'')))
#         dbsession_inst.executesql("insert into item_translations (item_uid, language_code, translation) values ('{}','{}','{}');" \
#                                 .format(n[4], tra.src, n[2].replace('\'', '\'\'')))
#     dbsession_inst.executesql('commit;')


def run():
    #clean_file_from_trash('D:\\Omen\\work\\Projects\\healthyFood\\dwh\\fitaudit.ru\\food\\100033\\amino.html')
    #beautify('D:\\Omen\\work\\Projects\\healthyFood\\dwh\\fitaudit.ru\\food\\100033.html')
    #beautifyall('D:\\Omen\\work\\Projects\\healthyFood\\dwh\\fitaudit.ru')
    #getdata('D:\\Omen\\work\\Projects\\healthyFood\\dwh\\fitaudit.ru\\food\\')

    #translate()

    # done
    # analize_tab('recepies')
    # analize_tab('recepies_instructions_cpy')
    # analize_tab('fa_product_category')
    # translate('recepies', 0, 2)
    # translate('recepies_instructions_cpy', 4, 2)
    # translate('fa_product_category', 5, 3)
    translate('item_translations', 0, 2)

    # donked


if __name__=='__main__':
    logger.info('Start work')
    run()
    logger.info('End work')