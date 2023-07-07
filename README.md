# shadowcopy

shadowcopy is a module for performing file copies from 'shadows' on Windows. Shadow copies are typically used to copy files that are locked for usage by other processes.

More info on shadow copies in Windows can be found [here](https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service)

Creating/Deleting shadown copies requires admin access.

## Installing

```
pip install shadowcopy
```

## Example

```
from shadowcopy import shadow_copy

# Internally this creates a shadow copy instance via WMI, copies the file, then deletes the shadow copy.
shadow_copy("source.txt", "destination.txt")
```
