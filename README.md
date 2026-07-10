# marketing_tag

## 구조
```
caret-html-macro/
├── main.py
├── requirements.txt
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── constants.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── mainWindow.py
│   │   └── settingsDialog.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── specParser.py
│   │   ├── htmlGenerator.py
│   │   ├── settingsService.py
│   │   └── fileService.py
│   │
│   └── models/
│       ├── __init__.py
│       └── contentData.py
│
├── config/
│   └── settings.json
│
├── templates/
│   ├── naver.html
│   ├── wordpress.html
│   └── companyMall.html
│
├── tests/
│   ├── __init__.py
│   ├── testSpecParser.py
│   └── testHtmlGenerator.py
│
└── output/
```