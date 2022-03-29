from django.http import HttpResponse
from django.shortcuts import render
from http.client import ResponseNotReady
from lxml import etree as ET
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from random import randint

from transaction.models import Transaction
from .serializers import PaymentSerializer


# Create your views here.
class TCIBViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def payment(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            transaction.status = 'PENDING'
            nsmap = {None: "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.05",                
                    "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
            root = ET.Element('Document', nsmap=nsmap)
            
            ftstmnt = ET.SubElement(root, 'FIToFICstmrCdtTrf')
            grbhdr = ET.SubElement(ftstmnt, 'GrpHdr')
            # Message ID
            msg_id = ET.SubElement(grbhdr, 'MsgId')
            msg_id.text =  f"IGW{datetime.now().strftime('%Y%m%d%H%M%S')}{randint(10000, 99999)}"
            # Transaction Date
            date = ET.SubElement(grbhdr, 'CreDtTm')
            current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            date.text = str(current_date)
            # Number of Transactions
            number_of_transactions = ET.SubElement(grbhdr, 'NbOfTxs')
            number_of_transactions.text = '1'
            # Settlement Information
            settlement_info = ET.SubElement(grbhdr, 'SttlmInf')
            settlement_mtd = ET.SubElement(settlement_info, 'SttlmMtd')
            settlement_mtd.text = 'CLRG'
            # Credit Information
            credit_info = ET.SubElement(ftstmnt, 'CdtTrfTxInf')
            payment_id = ET.SubElement(credit_info, 'PmtId')
            end_to_end_id = ET.SubElement(payment_id, 'EndToEndId')
            end_to_end_id.text = f"IGW{datetime.now().strftime('%Y%m%d%H%M%S')}{randint(10000, 99999)}"
            # Transaction ID
            transaction_id = ET.SubElement(payment_id, 'TxId')
            transaction_id.text = end_to_end_id.text
            # Payment Type Info
            payment_tpinf = ET.SubElement(credit_info, 'PmtTpInf')
            # Service Level
            service_level = ET.SubElement(payment_tpinf, 'SvcLvl')
            # Code
            credit = ET.SubElement(service_level, 'Cd')
            credit.text = 'URGP'
            # Interbank Settlement Acount
            inter_bank_settlement = ET.SubElement(credit_info, 'IntrBkSttlmAmt',Ccy=serializer.validated_data['amount']['currency_code'])
            inter_bank_settlement_date = ET.SubElement(credit_info, 'IntrBkSttlmDt',Ccy=serializer.validated_data['amount']['currency_code'])
            inter_bank_settlement.text = str(serializer.validated_data["amount"]["amount"])
            inter_bank_settlement_date.text = datetime.now().strftime('%Y-%m-%d')
            # Charge Bearer - Who is going to take care of the charge
            chrgbr = ET.SubElement(credit_info, 'ChrgBr')
            chrgbr.text = 'SLEV'
            # Debitor
            debitor = ET.SubElement(credit_info, 'Dbtr')
            # Debitor Name
            nm = ET.SubElement(debitor, 'Nm')
            nm.text = serializer.validated_data["sender"]["name"]
            # Debitor Postal Address
            pstladr = ET.SubElement(debitor, 'PstlAdr')
            street_number = ET.SubElement(pstladr, 'StrtNm')
            street_number.text = serializer.validated_data["sender"]["street_name"]

            post_code = ET.SubElement(pstladr, 'PstCd')
            post_code.text = serializer.validated_data["sender"]["postal_code"]

            town_name = ET.SubElement(pstladr, 'TwnNm')
            town_name.text = serializer.validated_data["sender"]["town_name"]

            country = ET.SubElement(pstladr, 'Ctry')
            country.text = serializer.validated_data["sender"]["country"]

            debitor_account = ET.SubElement(credit_info, 'DbtrAcct')
            id = ET.SubElement(debitor_account, 'Id')
            other = ET.SubElement(id, 'Othr')
            id_child = ET.SubElement(other, 'Id')
            id_child.text = serializer.validated_data["receiver"]["account_number"]
            # Debtor Agent - Financial Institution Processing the transaction
            debitor_agent = ET.SubElement(credit_info, 'DbtrAgt')
            financial_institution_id = ET.SubElement(debitor_agent, 'FinInstnId')
            bicfi = ET.SubElement(financial_institution_id, 'BICFI')
            bicfi.text = serializer.validated_data["participant_id"]
            # Creditor Agent - Financial Institution Servicing the account of the creditor
            creditor_agent = ET.SubElement(credit_info, 'CdtrAgt')
            cr_financial_institution_id = ET.SubElement(creditor_agent, 'FinInstnId')
            cr_bicfi = ET.SubElement(cr_financial_institution_id, 'BICFI')
            cr_bicfi.text = serializer.validated_data["receiving_agent_participant_id"]
            # Creditor Details
            creditor = ET.SubElement(credit_info, 'Cdtr')
            creditor_name = ET.SubElement(creditor, 'Nm')
            creditor_name.text = serializer.validated_data["receiver"]["name"]

            cr_postal_address = ET.SubElement(creditor, 'PstlAdr')
            
            cr_post_code = ET.SubElement(cr_postal_address, 'PstCd')
            cr_post_code.text = serializer.validated_data["receiver"]["postal_code"]
            
            cr_town_name = ET.SubElement(cr_postal_address, 'TwnNm')
            cr_town_name.text = serializer.validated_data["receiver"]["town_name"]

            cr_country_name = ET.SubElement(cr_postal_address, 'Ctry')
            cr_country_name.text = serializer.validated_data["receiver"]["country"]

            creditor_account = ET.SubElement(credit_info, 'CdtrAcct')
            cr_id = ET.SubElement(creditor_account, 'Id')
            cr_other = ET.SubElement(cr_id, 'Othr')
            cr_id_child = ET.SubElement(cr_other, 'Id')
            cr_id_child.text = serializer.validated_data["receiver"]["account_number"]
            # Regulatory Reporting Information 
            rgltryrptg = ET.SubElement(credit_info, 'RgltryRptg')
            dtls = ET.SubElement(rgltryrptg, 'Dtls')
            # Nature, Purpose and reason for the transaction
            cd = ET.SubElement(dtls, 'Cd')
            cd.text = '10402'
            # Payment Purpose/ Remmitance information - Unstructured
            rmtinf = ET.SubElement(credit_info, 'RmtInf')
            ustrd = ET.SubElement(rmtinf, 'Ustrd')
            ustrd.text = serializer.validated_data["purpose"]


            # print(ET.tostring(ftstmnt, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode())
            payload = HttpResponse(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone=True).decode(), content_type='text/xml')
            headers = {
                'Content-Type': 'text/xml',
                'X-AUTH-USER-NAME': 'IAS_USER',
                'X-AUTH-USER-PWD': 'b@nkse$v!23',
                'X-AUTH-API-VERSION': 'ISO20022v1.0'
            }
            url = "https://uat-tcib.bankservafrica.com:23211/eig/payment"
            response = request.post(url, data=payload, headers=headers)
            print(response.text)
            return payload
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def payment_return(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():           
            nsmap = {None: "urn:iso:std:iso:20022:tech:xsd:pacs.004.001.05",                
                    "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
            root = ET.Element('Document', nsmap=nsmap)
            
            ftstmnt = ET.SubElement(root, 'PmtRtr')
            grbhdr = ET.SubElement(ftstmnt, 'GrpHdr')
            # Message ID
            msg_id = ET.SubElement(grbhdr, 'MsgId')
            msg_id.text =  f"IGW{datetime.now().strftime('%Y%m%d%H%M%S')}{randint(10000, 99999)}"
            # Transaction Date
            date = ET.SubElement(grbhdr, 'CreDtTm')
            current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            date.text = str(current_date)
            # Number of Transactions
            number_of_transactions = ET.SubElement(grbhdr, 'NbOfTxs')
            number_of_transactions.text = '1'
            # Total Amount to be returned
            amount_to_be_returned = ET.SubElement(grbhdr, 'TtlRtrdIntrBkSttlmAmt',Ccy=serializer.validated_data['amount']['currency_code'])
            amount_to_be_returned.text = str(serializer.validated_data['amount']['amount'])
            # Settlement Date
            settlement_date = ET.SubElement(grbhdr, 'IntrBkSttlmDt')
            current_date_2 = datetime.now().strftime("%Y-%m-%d")
            settlement_date.text = str(current_date)
            # Settlement Information
            settlement_info = ET.SubElement(grbhdr, 'SttlmInf')
            settlement_mtd = ET.SubElement(settlement_info, 'SttlmMtd')
            settlement_mtd.text = 'CLRG'
            # Transaction Information
            credit_info = ET.SubElement(ftstmnt, 'TxInf')
            
            # Return ID
            rtd_id = ET.SubElement(credit_info, 'RtdId')
            rtd_id.text = 'Tests'
            # Original Group Information
            group_info = ET.SubElement(credit_info, 'OrgnlGrpInf')
            # Original Message ID
            original_message_id = ET.SubElement(group_info, 'OrgnlMsgId')
            original_message_id.text = 'Testtt'
            original_message_name_id = ET.SubElement(group_info, 'OrgnlMsgNmId')
            original_message_name_id.text = 'pacs.008.001.05'           
            # Original End to End ID
            origin_end_to_end = ET.SubElement(credit_info, 'OrgnlEndToEndId')
            origin_end_to_end.text = '567483'
            # Original Transaction ID
            origin_tx_id = ET.SubElement(credit_info, 'OrgnlTxId')
            origin_tx_id.text = '567483'
            # Original Amount
            original_amount = ET.SubElement(credit_info, 'OrgnlIntrBkSttlmAmt',Ccy=serializer.validated_data['amount']['currency_code'])
            original_amount.text = str(serializer.validated_data["amount"]["amount"])
            # Returned Amount
            original_amount = ET.SubElement(credit_info, 'RtrdIntrBkSttlmAmt',Ccy=serializer.validated_data['amount']['currency_code'])
            original_amount.text = str(serializer.validated_data["amount"]["amount"])
            # Return Reason Information
            return_reason = ET.SubElement(credit_info, 'RtrRsnInf')
            # Originator 
            original_transaction = ET.SubElement(return_reason, 'Orgtr')
            ID = ET.SubElement(original_transaction, 'Id')
            org_id = ET.SubElement(ID, 'OrgId')
            any_bic = ET.SubElement(org_id, 'AnyBIC')
            any_bic.text='1234'
            reason = ET.SubElement(return_reason, 'Rsn')
            code = ET.SubElement(reason, 'Cd')
            code.text = 'Test'
            # Original Transaction Reference
            original_ref = ET.SubElement(credit_info, 'OrgnlTxRef')
            settlement_date = ET.SubElement(original_ref, 'IntrBkSttlmDt')
            settlement_date.text = '2019-12-23'
             # Settlement Information
            settlement_info = ET.SubElement(original_ref, 'SttlmInf')
            settlement_mtd = ET.SubElement(settlement_info, 'SttlmMtd')
            settlement_mtd.text = 'CLRG'
            # Payment Type Info
            payment_tpinf = ET.SubElement(original_ref, 'PmtTpInf')
            # Service Level
            service_level = ET.SubElement(payment_tpinf, 'SvcLvl')
            # Code
            credit = ET.SubElement(service_level, 'Cd')
            credit.text = 'URGP'
             # Debitor
            debitor = ET.SubElement(original_ref, 'Dbtr')
            # Debitor Name
            nm = ET.SubElement(debitor, 'Nm')
            nm.text = serializer.validated_data["sender"]["name"]
            # Debitor Account
            debitor_account = ET.SubElement(original_ref, 'DbtrAcct')
            id = ET.SubElement(debitor_account, 'Id')
            other = ET.SubElement(id, 'Othr')
            id_child = ET.SubElement(other, 'Id')
            id_child.text = serializer.validated_data["receiver"]["account_number"]
            # Debtor Agent - Financial Institution Processing the transaction
            debitor_agent = ET.SubElement(original_ref, 'DbtrAgt')
            financial_institution_id = ET.SubElement(debitor_agent, 'FinInstnId')
            bicfi = ET.SubElement(financial_institution_id, 'BICFI')
            bicfi.text = serializer.validated_data["participant_id"]
            # Creditor Agent - Financial Institution Servicing the account of the creditor
            creditor_agent = ET.SubElement(original_ref, 'CdtrAgt')
            cr_financial_institution_id = ET.SubElement(creditor_agent, 'FinInstnId')
            cr_bicfi = ET.SubElement(cr_financial_institution_id, 'BICFI')
            cr_bicfi.text = serializer.validated_data["receiving_agent_participant_id"]
            # Creditor Details
            creditor = ET.SubElement(original_ref, 'Cdtr')
            creditor_name = ET.SubElement(creditor, 'Nm')
            creditor_name.text = serializer.validated_data["receiver"]["name"]
            # Creditor Account
            creditor_account = ET.SubElement(original_ref, 'CdtrAcct')
            cr_id = ET.SubElement(creditor_account, 'Id')
            cr_other = ET.SubElement(cr_id, 'Othr')
            cr_id_child = ET.SubElement(cr_other, 'Id')
            cr_id_child.text = serializer.validated_data["receiver"]["account_number"]
           

            # print(ET.tostring(ftstmnt, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode())
            return HttpResponse(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone=True).decode(), content_type='text/xml')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def status(self, request, msg_id=None):
        if msg_id is None:
            return Response({"message": "Message ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Message ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        transaction = Transaction.objects.get(msg_id=msg_id)
        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            response = generate_response('100', transaction.status)
            return Response(response, status=status.HTTP_200_OK)

