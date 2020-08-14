from gitgud import operations
from gitgud.skills.level_builder import BasicLevel
from gitgud.skills.util import Skill


class MergeConflicts(BasicLevel):
    def _test(self):
        if not super()._test():
            return False

        op = operations.get_operator()
        tree = op.repo.head.commit.tree
        merge_details = self.details()['M1']['files']

        for blob in tree.blobs:
            path = blob.path
            content = merge_details[path][0]
            blob_content = blob.data_stream.read().decode('ascii')

            if content.strip() != blob_content.strip():
                return False

        return True


skill = Skill(
    'Placeholder',
    'newbasics',
    [
    ]
)
