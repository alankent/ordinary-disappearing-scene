# Screen grab disappearing objects

This is a simple extension in response to
https://discord.com/channels/827959428476174346/975837676869656637/1253927583486316635

It takes a path (/World/Boxes) then does a screenshot, hiding one child
at a time until a screenshot is taken with all children hidden.

There is a RESET button which makes all the children visible again.

Output goes into 'outputs' under your Omniverse home directory.

I don't know how to pause for rendering to complete, so it currently
waits 10 frames. Seems to work.... (shiver!)
