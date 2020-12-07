#!/usr/bin/env python
#
# Paulo Sherring 2020
# Portions Copyright 2007 Neal Norwitz
# Portions Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

''' TODO:
    * Correct pointer positioning:
    void VIDEOIF::VIDEOIF_Layer::vSetPictureData(const  * VIDEOIN_tstPicData    pstPicdata)
                                                  ~~~~~~^This should be here: ^
    * Correct implementation calls:
    oVIDEOIF_Layer->vSetSendNextDecodedFrameMessage(bool boEnableSendNext);
                                                ~~~~~~^   This need to be dropped. Only call with variable name

    * Generate ctor and dtor on implementation file.                                                

'''

import argparse
import fnmatch
import os
import sys
import tempfile

from cpp import __version__
from cpp import ast
from cpp import tokenize
from cpp import utils


def match_file(filename, exclude_patterns):
    """Return True if file is a C++ file or a directory."""
    base_name = os.path.basename(filename)

    if base_name.startswith('.'):
        return False

    for pattern in exclude_patterns:
        if fnmatch.fnmatch(base_name, pattern):
            return False

    if find_warnings.is_header_file(filename):
        return True

    if find_warnings.is_cpp_file(filename):
        return True

    if os.path.isdir(filename):
        return True

    return False


def find_files(filenames, exclude_patterns):
    """Yield filenames."""
    while filenames:
        name = filenames.pop(0)
        if os.path.isdir(name):
            for root, directories, children in os.walk(name):
                filenames += [os.path.join(root, f) for f in sorted(children)
                              if match_file(os.path.join(root, f),
                                            exclude_patterns)]
                directories[:] = [d for d in directories
                                  if match_file(os.path.join(root, d),
                                                exclude_patterns)]
        else:
            yield name

def generate_mocked_header(entire_ast):
    # For Header File:
    HoutFile = ''
    for classNode in entire_ast:
        if isinstance(classNode,ast.Class):

            HoutFile += '#ifndef MOCK_{}_{}\n#define MOCK_{}_{}\n'.format(classNode.name.upper(),'H',classNode.name.upper(),'H')                   
            for namespacelevel in classNode.namespace:
                HoutFile += 'namespace %s\n{\n' % (namespacelevel)
            HoutFile += 'class %sMock:\n{\n'%(classNode.name)
            if classNode.body is not None:
                for funcNode in classNode.body:
                    if (isinstance(funcNode,ast.Function)):
                        if funcNode.return_type is not None:
                            # We don't generate mocked headers for Ctors and Dtors
                            HoutFile += "\tMOCK_METHOD%d(%s, %s%s);\n" % (len(funcNode.parameters), funcNode.name,funcNode.get_return_type(),funcNode.get_argument_signature_types())
                HoutFile += '} // endOfMockClass\n'
                for namespacelevel in reversed(classNode.namespace):
                    HoutFile += '} // namespace%s\n' % (namespacelevel)        
                #print(HoutFile)
                HoutFile += '#endif //MOCK_{}_{}\n\n'.format(classNode.name.upper(),'H')
            else:
                ''' Forward declaration only? let it be'''
                pass
            
        else:
            pass
    file = open('out.h','w')
    file.write(HoutFile)
    file.close()
    return HoutFile
        ##print('\n\n\n')

def generate_mocked_impl(entire_ast):
    
    ### For Implementation File:
    IoutFile = ''
    for classNode in entire_ast:
        if isinstance(classNode,ast.Class):
            IoutFile += '#include "mock_%s.h"\n#include "%s.h"\n' % (classNode.name.lower(),classNode.name.lower())

            IoutFile += '\nusing ::testing::NiceMock;\n'
            
            IoutFile += '\nstd::shared_ptr<NiceMock<'
            for namespacelevel in classNode.namespace:
                IoutFile += namespacelevel + '::'
            IoutFile += '%sMock>> o%s;\n\n' % (classNode.name,classNode.name)

            # for namespacelevel in classNode.namespace:
            #     IoutFile += 'namespace %s\n{\n' % (namespacelevel)
            IoutFile += '\n'
            if classNode.body is not None:
                for funcNode in classNode.body:
                    if (isinstance(funcNode,ast.Function)):
                        ret = ''
                        ret += funcNode.get_return_type()
                        for namespacelevel in funcNode.namespace:
                            ret += namespacelevel + '::'
                        ret += classNode.name
                        ret += '::' + funcNode.name + funcNode.get_argument_signature_types_names()
                        ret += '\n'
                        IoutFile += ret
                        ret = ''
                        if funcNode.return_type is None:
                            #Ctor, do nothing.
                            ret += '{\n\n}\n\n'
                        else:
                            if funcNode.return_type.name == 'void':
                                ret += '{\n\to%s->%s%s;\n}\n\n' % (classNode.name, funcNode.name, funcNode.get_argument_signature_names())
                            else:
                                ret += '{\n\treturn o%s->%s%s;\n}\n\n' % (classNode.name, funcNode.name, funcNode.get_argument_signature_names())
                        IoutFile += ret
                IoutFile += '} // endOfMockClass\n'
                IoutFile += '\n'
                # for namespacelevel in reversed(classNode.namespace):
                #     IoutFile += '} // namespace%s\n' % (namespacelevel)        
                #print(IoutFile)
        else:
            pass
    file = open('out.cpp','w')
    file.write(IoutFile)
    file.close()
    return IoutFile
    ##print('\n\n\n')

def mockFile(inputData):
    bHasTempFile = False
    if os.path.isfile(inputData):
        targetFile = inputData    
        bHasTempFile = False
    else:
        temporaryFile = tempfile.NamedTemporaryFile("w+",delete=False)
        temporaryFile.writelines(inputData)
        targetFile = temporaryFile.name
        temporaryFile.close()
        bHasTempFile = True
    try:
        source = utils.read_file(targetFile)
        if source is None:
            return None
        builder = ast.builder_from_source(source,
                                              targetFile,
                                              [],
                                              [],
                                              False)
        
        entire_ast = list([_f for _f in builder.generate() if _f])
        header = generate_mocked_header(entire_ast)
        impl = generate_mocked_impl(entire_ast)
            
    except tokenize.TokenError as exception:
        #print('{}: token error: {}'.format(targetFile, exception), file=sys.stderr)
        return '',''
    except (ast.ParseError, UnicodeDecodeError) as exception:
        #print('{}: parsing error: {}'.format(targetFile, exception), file=sys.stderr)
        return '',''
    if bHasTempFile == True:
        os.remove(targetFile)
    return header, impl

if __name__ == "__main__":
    try:
        sys.exit(mockFile('in.h'))
    except KeyboardInterrupt:
        sys.exit(1)
