def hide(address):
  return f'{(str(address)[:4]):*<{10}}'

def msg_formatter(msg):
  return f"\n{' ' + msg + ' ':-^{50}}\n"