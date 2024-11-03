import boto3

client = boto3.client(
    'textract',
    aws_access_key_id='',
    aws_secret_access_key='RX/+',
    region_name='ap-south-1'
    )


def analyze_invoice(document_path):
    with open(document_path, 'rb') as document:
        response = client.analyze_expense(
            Document={'Bytes': document.read()}
        )

    invoice_data = {}
    for expense_doc in response['ExpenseDocuments']:
        for field in expense_doc['SummaryFields']:
            label = field['Type']['Text']
            value = field['ValueDetection']['Text']
            invoice_data[label] = value

        line_items = []
        for line_item in expense_doc.get('LineItemGroups', []):
            for item in line_item['LineItems']:
                line = {field['Type']['Text']: field['ValueDetection']['Text'] for field in item['LineItemExpenseFields']}
                line_items.append(line)
        invoice_data['Line Items'] = line_items

    return invoice_data

document_path = "document2.jpg"
response = analyze_invoice(document_path)
print(response)
