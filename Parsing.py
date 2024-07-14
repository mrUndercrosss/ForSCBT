import xml.etree.ElementTree as ET
from Debtor import write_info_debtor
from ExtrajudicialBankruptcyMessage import write_info_message
from MonetaryObligation import write_info_monetary_obligation
from ObligatoryPayment import write_info_obligation_payment
from Bank import write_info_bank


def get_element_text(element, tag, default=None):
    """
    Функция для получения текстового содержимого элемента XML.
    Если элемент не найден или его текстовое содержимое отсутствует,
    возвращается значение по умолчанию.
    """
    elem = element.find(tag)
    if elem is not None and elem.text is not None:
        return elem.text.strip()
    else:
        return default


def read_data(file_path, db_uri):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []
    for message in root.findall('ExtrajudicialBankruptcyMessage'):
        message_id = get_element_text(message, 'Id')
        number = get_element_text(message, 'Number')
        message_type = get_element_text(message, 'Type')
        publish_date = get_element_text(message, 'PublishDate')

        debtor = message.find('Debtor')
        debtor_name = get_element_text(debtor, 'Name')
        birth_date = get_element_text(debtor, 'BirthDate')
        birth_place = get_element_text(debtor, 'BirthPlace')
        debtor_inn = get_element_text(debtor, 'Inn')
        address = get_element_text(debtor, 'Address')
        debtor_snils = get_element_text(debtor, 'Snils')

        name_history = []
        for previous_name in debtor.findall('.//PreviousName'):
            name_history.append(get_element_text(previous_name, 'Value'))

        publisher = message.find('Publisher')
        publisher_name = get_element_text(publisher, 'Name')
        publisher_inn = get_element_text(publisher, 'Inn')
        publisher_ogrn = get_element_text(publisher, 'Ogrn')

        finish_reason = get_element_text(message, 'FinishReason')

        obligations = []
        for obligation in message.findall('.//MonetaryObligation'):
            creditor_name = get_element_text(obligation, 'CreditorName')
            content = get_element_text(obligation, 'Content')
            basis = get_element_text(obligation, 'Basis')
            total_sum = get_element_text(obligation, 'TotalSum')
            debt_sum = get_element_text(obligation, 'DebtSum')
            penalty_sum = get_element_text(obligation, 'PenaltySum', '0')
            obligations.append({
                'CreditorName': creditor_name,
                'Content': content,
                'Basis': basis,
                'TotalSum': total_sum,
                'DebtSum': debt_sum,
                'PenaltySum': penalty_sum})

        obligation_payment = []
        for payment in message.findall('.//ObligatoryPayment'):
            payment_name = get_element_text(payment, 'Name')
            payment_sum = get_element_text(payment, 'Sum')
            payment_penalty_sum = get_element_text(payment, 'PenaltySum', '0')
            obligation_payment.append({
                'PaymentName': payment_name,
                'PaymentSum': payment_sum,
                'Payment_penalty_sum': payment_penalty_sum})

        bank = []
        for enter in message.findall('.//Bank'):
            bank_name = get_element_text(enter, 'Name')
            bik = get_element_text(enter, 'Bik')
            bank.append({
                'BankName': bank_name,
                'BIK': bik})

        data.append({
            'MessageId': message_id,
            'Number': number,
            'MessageType': message_type,
            'PublishDate': publish_date,
            'DebtorName': debtor_name,
            'DebtorBirthDate': birth_date,
            'DebtorBirthPlace': birth_place,
            'DebtorInn': debtor_inn,
            'DebtorAddress': address,
            'DebtorSnils': debtor_snils,
            'NameHistory': name_history,
            'PublisherName': publisher_name,
            'PublisherInn': publisher_inn,
            'PublisherOgrn': publisher_ogrn,
            'FinishReason': finish_reason,
            'Obligations': obligations,
            'ObligationPayment': obligation_payment,
            'Bank': bank
        })

    write_info_debtor(data, db_uri)
    write_info_message(data, db_uri)
    write_info_monetary_obligation(data, db_uri)
    write_info_obligation_payment(data, db_uri)
    write_info_bank(data, db_uri)

