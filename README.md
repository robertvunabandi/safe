# Safe File Storage

This is a tool to save encrypted files with password. 

If a file is named `myfile.extension`, the `safe` file will be named `myfile.extension.safe`. 

To encrypt a file, one can run:
```bash
safe convert path/to/file.extension
```
This would create the file `path/to/file.extension.safe`, which would be encrypted. 

One can open and run a command on a `.safe` file via `shell` command, like this 
for Vim for instance:

```bash
safe shell path/to/file.safe --vim 
```
