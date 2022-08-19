# Custom pages folder

## File structure
```
custom_pages
└─ $PROJECT_NAME
   └─ $TEST_NAME
      └─ $SUBDIR
         └─ index.html | index.js | index.css (mandatory)
         └─ headers.json (optional)
```

The custom web page is hosted under the path `/custom/$TEST_NAME/$SUBDIR`.

## Important rules
- `$TEST_NAME` should be unique over all projects!