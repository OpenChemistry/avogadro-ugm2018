Generators & Command Scripts
=======

Input Generators and Command scripts work similarly - passing JSON to Avogadro to render a form interface and then perform work. In principal, the scripts can be written in any programming language, although most are currently written in Python.

This guide will cover the UI aspects of scripts, with separate discussion of generators and command operation elsewhere.

## Script Entry Points

The script *must* handle the following command-line arguments:

* `--debug` Enable extra debugging output. Used with other commands. It is not required that the script support extra debugging, but it should not crash when this option is passed.
* `--lang XX` Display the user interface with a specific language or localization. It is not required that scripts support localization, but it should not crash when this option is passed.
* `--print-options` Print the available UI options supported by the script, e.g. simulation parameters, etc. See below for more details.
* `--display-name` Print a user-friendly name for the script. This is used in the GUI for menu entries, window titles, etc.
* `--menu-path` Print the expected menu path for the script, separated by "|" characters (e.g., "Extensions|Quantum" or "Build|Insert"). The final part of the menu path will include the display-name.


## Specifying UI options with --print-options

The format of the `--print-options` output must be a JSON object of the following form:

```
{
  "userOptions": {
    ...
  },
  "highlightStyles": [
    {
      "style": "Descriptive name",
      "rules": [
        {
          "patterns": [ ... ],
          "format": { ... }
        },
        ...
      ],
    },
    ...
  ],
  "inputMoleculeFormat": "cjson"
}
```

The `userOptions` block contains a JSON object keyed with option names (e.g. "First option name"), which are used in the GUI to label simulation parameter settings. Various parameter types are supported:

### Fixed String Lists (Pop-up menus)

Parameters that have a fixed number of mutually-exclusive string values will be presented using a popup menu (combo box). Such a parameter can be specified in the `userOptions` block as:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "stringList",
      "values": ["Option 1", "Option 2", "Option 3"],
      "default": 0
    }
  }
}
```

Here, "Parameter Name" is the default label that will be displayed in the GUI as a label next to the combo box. If you wish to have the label differ from the JSON key, you can add a "label" key pair:

```
"userOptions": {
  "element": {
    "type": "stringList",
    "label": "Metal",
    "values": ["Gold", "Silver", "Platinum"],
    "default": 0
  }
}
```

Use of the "label" is optional, but encouraged, since it greatly facilitates translation and localization (e.g., "color" vs. "colour").

The array of strings in values will be used as the available entries in the combo box in the order they are written. The default parameter is a zero-based index into the values array and indicates which value should be initially selected.

### Short Free-Form Text Parameters

A short text string can be requested (e.g. for the "title" of an optimization) via:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "string",
      "default": "blah blah blah"
    }
  }
}
```

This will add a blank text box to the GUI, initialized with the text specified by default.

### Existing files

A script can ask for the absolute path to an existing file using the following option block:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "filePath",
      "default": "/path/to/some/file"
    }
  }
}
```

This will add an option to select a file to the GUI, initialized to the file pointed to by default.

### Integer Values

Scripts may request integer values from a specified range by adding a user-option of the following form:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "integer",
      "minimum": -5,
      "maximum": 5,
      "default": 0,
      "prefix": "some text ",
      "suffix": " units"
    }
  }
}
```

This block will result in a QSpinBox, configured as follows:

* minimum and maximum indicate the valid range of integers for the parameter.
* default is the integer value that will be shown initially.
* (optional) prefix and suffix are used to insert text before or after the integer value in the spin box. This is handy for specifying units. Note that any prefix or suffix will be stripped out of the corresponding entry in the call to scripts, and just the raw integer value will be sent.

### Floating-point values

Scripts may request floating-point values from a specififed range by adding a user-option of the following form:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "float",
      "minimum": -5,
      "maximum": 5,
      "default": 0,
      "precision": 3,
      "prefix": "some text ",
      "suffix": " units"
    }
  }
}
```

This block will result in a QSpinBox, configured as follows:

* minimum and maximum indicate the valid range of float for the parameter.
* default is the float value that will be shown initially.
* precision is the significant figures of the floating-point value
* (optional) prefix and suffix are used to insert text before or after the float value in the spin box. This is handy for specifying units. Note that any prefix or suffix will be stripped out of the corresponding entry in the call to scripts, and just the raw float value will be sent.

### Boolean Parameters

If a simple on/off value is needed, a boolean type option can be requested:

```
{
  "userOptions": {
    "Parameter Name": {
      "type": "boolean",
      "default": True,
    }
  }
}
```

This will result in a check box in the dynamically generated GUI, with the initial check state shown in default.



### Special Parameters

Some parameters are common to most calculation codes. If the following parameter names are found, they will be handled specially while creating the GUI. It is recommended to use the names below for these options to provide a consistent interface and ensure that MoleQueue job staging uses correct values where appropriate.

| Option name | Type | Description |
| :---: | :----: | :-- |
| "Title" | string | Input file title comment, MoleQueue job description. |
| "Filename Base" | string | Input file base name, e.g. "job" in "job.inp". |
| "Processor Cores" | integer | Number of cores to use. Will be passed to MoleQueue. |
| "Calculation Type" | stringList | Type of calculation, e.g. "Single Point" or "Equilibrium Geometry". |
| "Theory" | stringList | Levels of QM theory, e.g. "RHF", "B3LYP", "MP2", "CCSD", etc. |
| "Basis" | stringList | Available basis sets, e.g. "STO-3G", "6-31G**", etc. |
| "Charge" | integer | Charge on the system. |
| "Multiplicity" | integer | Spin multiplicity of the system. |



### Requesting Full Structure of Current Molecule

The `inputMoleculeFormat` key is optional, and can be used to request a representation of the current molecule's geometry when --generate-input is called. The corresponding value indicates the format of the molecule that the script expects. If this value is omitted, no representation of the structure will be provided.
