from urllib.parse import urlparse, parse_qsl


def extract_src_ctz(url: str) -> str:
    calendar_url = 'https://calendar.google.com/calendar'
    if calendar_url in url:
        url = url[url.index(calendar_url):]
        parsed_url = urlparse(url)
        query_params = parse_qsl(parsed_url.query)
        new_query = ''
        for key, value in query_params:
            if key in ['src', 'ctz']:
                value = value.split()[0].replace("'", "").replace('"', '')
                new_query += f'&{key}={value}'
        return new_query.lstrip('&')
    return ''
