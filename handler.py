import json
import re
import smtplib
import dns.resolver

def verify(event, context):
    verification_address = event['queryStringParameters']['email']
    from_address = 'btmash@gmail.com'
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
    match = re.match(regex, verification_address)
    if (match == "None"):
        body = {
            'message': 'Bad Syntax',
            'status': 'FALSE'
        }
    else:
        split_verfication_address = verification_address.split('@')
        domain = str(split_verfication_address[1])
        records = dns.resolver.query(domain, 'MX')
        mx_record = records[0].exchange
        mx_record = str(mx_record)
        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        # SMTP Conversation
        server.connect(mx_record)
        server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
        server.mail(from_address)
        code, message = server.rcpt(str(verification_address))
        server.quit()
        if (code == 250):
            body = {
                'message': 'Valid email',
                'status': 'TRUE'
            }
        else:
            body = {
                'message': 'Invalid email',
                'status': 'FALSE'
            }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
