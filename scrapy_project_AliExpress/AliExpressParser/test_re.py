import re

ss = ' (796 результатов)'

pattern = 'результатов'

if re.search(pattern, ss) is not None:
    print('Соответствует')
else:
    print('Не соответствует')
