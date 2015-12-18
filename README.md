# python-json-server
json server implemented by python

## Usage 

```
Usage: pjs.py [Options] config

Options:
  -h, --help  show this help message and exit
  -v          print all information

config  file used for router and response customization
```
  
## Features
*  json-string response, written in json-data-file
*  config response code, e.g 200, 500
*  route different request path according to path key

## Demo
Following is the demo config file.  

```
port = 3001
response_code = 210

[user]
response_file = demo_response_user.json
response_code = 200

[order]
response_file = demo_response_order.json
response_code = 200
```

The section without section header is treat as global config. It can config following options.  

* `host`  Defining the host, e.g `localhost`
* `port`  Defining port for the server, e.g `3000`
* `response_code`  Defining response code for global response, e.g `200`

[section_name] is each section head. And at the same time, it will be treat as route path key. 
For example, `[user]` means the url path containing user will be route to this section and will be replied by configuration of this section.  

Each section contains following options.  

* `response_file`  This defines a json file containing json string for response.
* `response_code`  This defines a response code for the response.

If one section lacks one option, the global counterpart will be used as default. But response_file cannot be omit, otherwise, the section would be useless.
