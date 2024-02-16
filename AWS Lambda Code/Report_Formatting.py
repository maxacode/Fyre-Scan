import boto3

def generate_html_report(file_content):
    # Split file content into lines
    lines = file_content.split('\n')
    
    # Extract information from the lines
    service_info = []
    for line in lines:
        parts = line.split(',')
        if len(parts) == 5:  #IP, service, port, version, CVEs
            service_info.append(parts)
    
    # Generate HTML report
    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>FyreScanner Report</title>
    </head>
    <body>
    <h1>FyreScanner</h1>
    <h2>Client Name:</h2>
    <h2>Date of Scan:</h2>
    <h2>Client IP:</h2>
    <hr>
    """
    
    for info in service_info:
        ip, service, port, version, cves = info
        html += f"<h3>Service Running: {service}</h3>\n"
        html += f"<p>Port: {port}</p>\n"
        html += f"<p>Version: {version}</p>\n"
        html += f"<p>CVE: {cves}</p>\n"
        # Additional fields like Risk Category and Remediation can be added here
        html += "<p>Recommendations:</p>\n"
        html += "<hr>\n"
    
    html += "<p>--End of Report--</p>\n"
    html += "</body>\n</html>"
    
    return html

def lambda_handler(event, context):
    # Get the input TXT file from the unformatted_reports folder in the fyrescanner bucket
    input_bucket = 'fyrescanner'
    input_key = event['Records'][0]['s3']['object']['key']
    
    if not input_key.startswith('unformatted_reports/'):
        return {
            'statusCode': 400,
            'body': 'TXT file should be placed in the unformatted_reports folder'
        }
    
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=input_bucket, Key=input_key)
    file_content = response['Body'].read().decode('utf-8')
    
    html_content = generate_html_report(file_content)
    
    # Upload HTML file to the Final_reports folder
    output_key = input_key.replace('unformatted_reports/', 'Final_reports/').replace('.txt', '.html')
    s3_client.put_object(Bucket=input_bucket, Key=output_key, Body=html_content.encode('utf-8'), ContentType='text/html')
    
    return {
        'statusCode': 200,
        'body': 'Conversion Successful'
    }
