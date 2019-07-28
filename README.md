# Safe File Storage

This is a tool to save encrypted files with password. 

If a file is named `myfile.extension`, the `safe` file will be named `myfile.extension.safe`. 

One can open and edit a `.safe` file via `Vim` using any of the following:

```bash
safe --vim path/to/file.safe -p passcode
safe --vi path/to/file.safe -p passcode
safe -v path/to/file.safe -p passcode
```

```bash
"create a path/to/file.extension.safe that is protected with this user's passcode
safe path/to/file.extension 
```
