Input Generators
========

Input generators offer several unique capabilities for formatting text input
for programs, including syntax highlighting rules and capabilities for creating
multiple files as part of one input (e.g., separate files for geometry and keywords).

### Syntax Highlighting

Rules for syntax highlighting can be specified as a collection of regular expressions or wildcard patterns and text format specifications in the "highlightRules" array. The highlightRules format is:

```
"highlightStyles": [
  {
    "style": "Style 1",
    "rules": [ (list of highlight rules, see below) ],
  },
  {
    "style": "Style 2",
    "rules": [ (list of highlight rules, see below) ],
  },
  ...
],
```

The style name is unique to the style object, and used to associate a set of highlighting rules with particular output files. See the --generate-input documentation for more details.

The general form of a highlight rule is:
```
{
  "patterns": [
    { "regexp": "^Some regexp?$" },
    { "wildcard": "A * wildcard expression" },
    { "string": "An exact string to match.",
      "caseSensitive": false
    },
    ...
  ],
  "format": {
    "preset": "<preset name>"
  }
}
```
or,
```
{
  "patterns": [
    ...
  ],
  "format": {
    "foreground": [ 255, 128,  64 ],
    "background": [   0, 128, 128 ],
    "attributes": ["bold", "italic", "underline"],
    "family": "serif"
  }
}
```
The patterns array contains a collection of fixed strings, wildcard expressions, and regular expressions (using the QRegExp syntax flavor, see the QRegExp documentation) that are used to identify strings that should be formatted. There must be one of the following members present in each pattern object:

* regexp A QRegExp-style regular expression. If no capture groups ("(...)") are defined, the entire match is formatted. If one or more capture groups, only the captured texts will be marked.
* wildcard A wildcard expression
* string An exact string to match.
Any pattern object may also set a boolean caseSensitive member to indicate whether the match should consider character case. If omitted, a case-sensitive match is assumed.

The preferred form of the format member is simply a specification of a preset format. This allows for consistent color schemes across input generators. The recognized presets are:

* "title": A human readable title string.
* "keyword": directives defined by the target input format specification to have special meaning, such as tags indicating where coordinates are to be found.
* "property": A property of the simulation, such as level of theory, basis set, minimization method, etc.
* "literal": A numeric literal (i.e. a raw number, such as a coordinate).
* "comment": Sections of the input that are ignored by the simulation code.

If advanced formatting is desired, the second form of the format member allows fine-tuning of the font properties:

* foreground color as an RGB tuple, ranged 0-255
* background color as an RGB tuple, ranged 0-255
* attributes array of font attributes, valid strings are "bold", "italic", or "underline"
* family of font. Valid values are "serif", "sans", or "mono"
Any of the font property members may be omitted and default QTextCharFormat settings will be substituted.

The input generator extension will apply the entries in the highlightRules object to the text in the order they appear. Thus, later rules will override the formatting of earlier rules should a conflict arise.
