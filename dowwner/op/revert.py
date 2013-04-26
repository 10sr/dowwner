#!/usr/bin/env python3

import dowwner.op.edit

class ContentGET(dowwner.op.edit.ContentGET):
    """Revert class."""
    def main(self):
        """
        Args:
            storage: Storage object.
            path_: Path object.
        """
        orig = self.storage.load_bak(self.path, raw=True)
        dowwner.op.edit.ContentGET.main(self, orig=orig,
                                        target=self.path.base.partition(".")[2])
        self.pagename = "revert: " + self.path.path
        return
