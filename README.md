# templator
This is a very simple yet useful utility to generate files based on a template and a dictionary of replacements because I could not find such a tool readily available and it looked quite easy to do myself. It takes a template file and a JSON formatted replacement file as input and produces an output file for each entry. Notably it is secure against format-string attacks, so it is principly possible to have untrusted user input in the template and replacement files as well as the name template. (Note that this still might lead to problems like [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting) depending on your use case).

Idk if this is useful or not but I am going to share it anyways just because. It is light (<100 LOC), well-written and secure.

## Usage
To use the utility, clone the git repository and run the Python script. Use `templator.py --help` to see all available options. You can also find an [example](#example) at the end.

```
git clone 'https://github.com/AntiKippi/templator.git'
cd templator
python templator.py --help
```

## Output
The resulting files are written into the specified directory and named after the given name template. The name template format is exactly the same as the file template format, so see [Template Format](#template-format) for details. All keys of the replacement dictionary can be used.

If you wonder why the default extension is `.html`: Because I say so. I use this to generate HTML pages so it's handy for me.

## Template format
The template is basicly a Python [`string.Template`](https://docs.python.org/3.13/library/string.html#string.Template) template string. As such:
 - All occurrences of `$key` will be replaced with the respective value if "`key`" is found in the replacement entry. Key RegEx (case-insensitive): `[_a-z][_a-z0-9]*`.
 - Dollars are escaped with `$$`, so `$$key` will just become `$key` without undergoing replacement.
 - Keys can be put into curly braces to avoid text directly after the key getting interpreted as part of the key. Example: `some${key}inside`.
 - If a `$key` expression has no corresponding key-value pair in the replacement entry it will stay unmodified.

## Replacement file format
The replacements file is a simple JSON array of replacement objects. Each replacement object is a list of key-value pairs where when `key` is found in the template it is replaced by `value`. Any key-value pairs without corresponding key in the template will just be ignored.

## Example

`$ cat template.html`
```html
<html>
<head>
  <meta charset="UTF-8">
  <title>$code - $reason_phrase</title>
</head>
<body>
  <h1>${code}_ERROR</h1>
  <p>$$reason_phrase: $reason_phrase</p>
  <p>$error_description: $desc</p>
</body>
</html>
```
`$ cat rep.json`
```json
[
  {
    "code": 404,
    "reason_phrase": "Not Found",
    "desc": "The page you requested does not exist.",
    "unused": "An unused key."
  },{
    "code": 403,
    "reason_phrase": "Forbidden"
  }
]
```
`$ templator.py -k code -t template.html -r rep.json`  
`$ cat 404.html`
```html
<html>
<head>
  <meta charset="UTF-8">
  <title>404 - Not Found</title>
</head>
<body>
  <h1>404_ERROR</h1>
  <p>$reason_phrase: Not Found</p>
  <p>$error_description: The page you requested does not exist.</p>
</body>
</html>
```
`$ cat 403.html`
```html
<html>
<head>
  <meta charset="UTF-8">
  <title>403 - Forbidden</title>
</head>
<body>
  <h1>403_ERROR</h1>
  <p>$reason_phrase: Forbidden</p>
  <p>$error_description: $desc</p>
</body>
</html>
```