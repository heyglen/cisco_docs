
from cisco_doc.utilities.dot_dict import DotDict


parser = DotDict({
    'nxos': {
        'anchor_prefix' : 'pgfId-',
        'command': {
            'syntax' : {
                'element': 'p',
                'class_': 'pCENB_CmdEnv_NoBold',
            },
            'description' : {
                'element': 'p',
                'class_': 'pB1_Body1',
            },
            'keyword': {
                'classes': [
                    'cCN_CmdName',
                    'cKeyword',
                    'cBold',
                ],
            },
            'argument': {
                'classes': [
                    'cArgument',
                    'cEmphasis',
                    'cCi_CmdItalic',
                ],
            },
        },
    },
})