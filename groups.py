import re

domain_service_list = {
    'github.com': 'GitHub',
    'twitter.com': 'Twitter',
    'atlassian.com': 'Atlassian',
    'youtube.com': 'YouTube',
    'bitbucket.org': 'BitBucket',
    'outlook.live.com': 'Outlook',
    'google.com': 'Google'
}

ip_list = {
    '192.168.1.11': 'Mac Studio',
    '192.168.1.3': 'PC2',
    '192.168.1.20': 'rasberry pi',
}


def get_group(ip_or_host: str) -> str:
    if is_ip(ip_or_host):
        return ip_list[ip_or_host] if ip_or_host in ip_list else ip_or_host
    return aggregate_host(ip_or_host.rstrip('.'))


def aggregate_host(host: str) -> str:
    group = [v for k, v in domain_service_list.items() if k in host]
    return group[0] if len(group)>=1 else host


def is_ip(ip_or_host: str) -> bool:
    return is_ip_v4(ip_or_host) or is_ip_v6(ip_or_host)


# 厳密なチェックじゃなくていい
def is_ip_v4(ip_or_host: str) -> bool:
    pattern = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    return re.match(pattern, ip_or_host)


def is_ip_v6(ip_or_host: str) -> bool:
    # どうせここにくるのはIPかドメイン名で、ドメイン名に `:` は使えない
    return ip_or_host.count(':') >= 2

if __name__ == "__main__":
  print(get_group('192.168.1.1'))
  print(get_group('192.168.1.3'))
  print(get_group('github.com.'))
  print(get_group('avatar.github.com.'))
  for k,v in domain_service_list.items():
    print(k, v)
    if 'github.com.' in k:
      print(v)