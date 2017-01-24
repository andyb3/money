import xml.etree.ElementTree as etree
import datetime
from decimal import Decimal

class ofxData(object):
    '''Imports data from OFX file for money Django app'''
    def __init__(self, ofxPath):
        self.ofxPath = ofxPath
    def statementDetails(self):
        try:
            tree = etree.parse(self.ofxPath)
            account = tree.find('./BANKMSGSRSV1/STMTTRNRS/STMTRS/BANKACCTFROM/ACCTID').text
            period_start = tree.find('./BANKMSGSRSV1/STMTTRNRS/STMTRS/BANKTRANLIST/DTSTART').text
            period_start =  datetime.datetime.strptime(period_start[:8], '%Y%m%d').date()
            period_end = tree.find('./BANKMSGSRSV1/STMTTRNRS/STMTRS/BANKTRANLIST/DTEND').text
            period_end =  datetime.datetime.strptime(period_end[:8], '%Y%m%d').date()
            return {'account': account,
                    'period_start': period_start,
                    'period_end': period_end
                    }
        except:
            return "error"
    def transDetails(self):
        try:
            tree = etree.parse(self.ofxPath)
            balance = Decimal(tree.find('./BANKMSGSRSV1/STMTTRNRS/STMTRS/LEDGERBAL/BALAMT').text)
            allTrans = tree.findall('./BANKMSGSRSV1/STMTTRNRS/STMTRS/BANKTRANLIST/STMTTRN')
            lstTrans = []
            for trans in allTrans[::-1]:
                tx_type = trans.find('./TRNTYPE').text
                tx_date = trans.find('./DTPOSTED').text
                tx_date = datetime.datetime.strptime(tx_date[:8], '%Y%m%d').date()
                ofx_txID = trans.find('./FITID').text
                description = trans.find('./NAME').text
                amount = Decimal(trans.find('./TRNAMT').text)
                lstTrans.append({'tx_type': tx_type,
                                'date': tx_date,
                                'ofx_txID': ofx_txID,
                                'description': description,
                                'amount': amount,
                                'balance': balance
                                })
                balance -= amount
            lstTrans.reverse()
            return lstTrans
        except:
            return "error"

if __name__ == '__main__':
    filepath = '/home/andy/Downloads/Statement Download 2017-Jan-09 21-10-09.ofx'
    o = ofxData(filepath)
    transDets = o.transDetails()
    if transDets == "error":
        print("ERRROOOOORRRR")
    else:
        print("NOOOOOOOOOOOO err")
