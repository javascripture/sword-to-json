# sword-to-json

**Python utility to convert Crosswire sword bible modules to JSON**



<br>

## Introduction

`sword-to-json` [dumbly](#limitations) converts [Crosswire sword bible modules](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles "Jesus loves you") to JSON.

It does some minimalistic tidying up of verse data - trimming, removing double spaces, etc



<br>

## Examples

Check out the [bibles](/bibles "Jesus loves you") folder for examples of bible JSON generated using `sword-to-json`



<br>

## Usage

You can use `sword-to-json` to generate JSON from any sword module as follows:

(1) Install [Python 3](https://www.python.org/downloads "Jesus loves you")

(2) Git clone this repo .. `git clone git@github.com:danday74/sword-to-json.git`

(3) Move to the root folder .. `cd sword-to-json`

(4) Place the ZIP file for any sword module you want to convert into the [sword-modules](/sword-modules) folder

NOTE: Download sword module ZIP files from [crosswire](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles "Jesus loves you") or [ebible](http://ebible.org/find  "Jesus loves you")

(5) run .. `python sword_to_json.py`

(6) Wait for processing to complete

(7) The JSON for your chosen sword modules will appear in the [bibles](/bibles "Jesus loves you") folder



<br>

## Advanced Usage

For step (5) above you can run any of the following:

`python sword_to_json.py` - Creates JSON for sword modules, skipping modules for which the JSON already exists

`python sword_to_json.py --overwrite` - Creates JSON for sword modules without skipping

`python sword_to_json.py --partials` - Creates JSON and partial JSON for sword modules, skipping modules for which the JSON already exists

NOTE: partial JSON only shows some of the data and is pretty printed. It only exists to help you understand the structure of the JSON and is otherwise useless.

`python sword_to_json.py --overwrite --partials` - Creates JSON and partial JSON for sword modules without skipping



<br>

## Limitations

`sword-to-json` does not attempt to fix sword verse data but dumbly provides data as is.

For example, using the KJV sword module, [Romans 16:27 KJV](https://www.blueletterbible.org/kjv/rom/16/27/s_1062027 "Jesus loves you") reads:

> To God only wise, be glory through Jesus Christ for ever. Amen. Written to the Romans from Corinthus, and sent by Phebe servant of the church at Cenchrea.

Whereas it should read:

> To God only wise, be glory through Jesus Christ for ever. Amen.

The additional text being present in the KJV but not forming part of the verse itself.



<br>

## Author Says

In case you weren't listening the first time, let me say it again:

> To God only wise, be glory through Jesus Christ for ever. Amen.

[Romans 16:27 KJV](https://www.blueletterbible.org/kjv/rom/16/27/s_1062027 "Jesus loves you")



<br><br><br>
