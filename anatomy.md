"""
            Implementation mock anatomy:
            
            #include "{MOCK_H}"
            #include "{IMPLEMENTATION_H}"

            using ::testing::NiceMock;
            
            std::shared_ptr<NiceMock<{NAMESPACELIST}::{CLASSNAME}MockInterfaceManagerMock>> o{CLASSNAME};

            namespace {NAMESPACE#1}
            {
            namespace {NAMESPACE#2}
            {

                {CLASSNAME}::CTOR();

                {CLASSNAME}::~DTOR()

                {CLASSNAME}::{FUNCTIONNAME}({ARGLIST})
                {
                    IF retval not void:
                        return o{CLASSNAME}->{FUNCTIONNAME}({ARGLIST});
                    ELSE:
                        o{CLASSNAME}->{FUNCTIONNAME}({ARGLIST});
                }
                ...
                class {ClassName}Mock:
                {
                    MOCK_METHOD{argCount}({MethodName},{ReturnType}(argListTypes));
                    MOCK_METHOD{argCount}({MethodName},{ReturnType}(argListTypes));
                    ...
                };

            } //{NAMESPACE#2}

            } //{NAMESPACE#1}
            """




                        """
            header mock anatomy:

            #ifndef MOCK_{FILENAME_WITHOUT_EXT}_{EXT}
            #define MOCK_{FILENAME_WITHOUT_EXT}_{EXT}

            originalIncludes?

            namespace {NAMESPACE#1}
            {
            namespace {NAMESPACE#2}
            {
                ...
                class {ClassName}Mock:
                {
                    MOCK_METHOD{argCount}({MethodName},{ReturnType}(argListTypes));
                    MOCK_METHOD{argCount}({MethodName},{ReturnType}(argListTypes));
                    ...
                };

            } //{NAMESPACE#2}

            } //{NAMESPACE#1}
            #endif //MOCK_{FILENAME_WITHOUT_EXT}_{EXT}
            """