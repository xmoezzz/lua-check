LuaQ                #°     A@    À@@  A@ @   A @   AÀ @   A  @   A@ @   A @   AÀ  E    \   Á@  ÁÀ Ç Á@ Ç  Á Ç Ê   ÇÀ ÅÀ É EÅÀ ÉÅÅÀ É ÆÅÀ ÉÆÅÀ É ÇÅÀ ÉÇÅÀ É ÈÅÀ ÉÈÅÀ É ÉÅÀ ÉÉÅÀ É ÊÅÀ ÉÊÅÀ É ËÅÀ ÉËÅÀ É ÌÅÀ ÉÌÅÀ ÉÇÅÀ É MÅÀ É@ÍÅÀ ÉMÅÀ ÉÀÍÅÀ É@NÅÀ ÉÀNÅÀ É@OÁÀ Ç Ã Ç  Â   Ç@ Á Á A A Á Â A Â ÁB Ã A Ã ÁC  AD  ÁD  AÅ Å ÁÅ F AF F ÁF Ç A G Á È A ¤      H ¤H       ¤      È ¤È       ¤      	    H ¤H      ¤               	È ¤È      	     ¤     H ¤H            	   	 ¤      	    È ¤È      ¤               	H ¤H      	     ¤     È ¤È      ¤      	       H ¤H      	     ¤     È ¤È               	 ¤      	    H ¤H      ¤            	   	È ¤È      	     ¤     H ¤H               	 ¤      	    È ¤È      ¤          	  H ¤H      	        ¤      	    È ¤È      ¤               	H ¤H      	     ¤     È ¤È            	   	 ¤	      	    H ¤H	      ¤	               	È ¤È	      	     ¤
     H ¤H
      	       ¤
      	       È ¤È
      	      ¤     H  ¤H               	  ¤      	    È  ¤È     ! ¤              	                          	H! ¤H     ! ¤     È! ¤È     " ¤          H" ¤H          " ¤     È" ¤È      
       # ¤                     
                   H# ¤H                                # ¤     È#         module $   com.teamf1.core.authentication.pop3    package    seeall    require    teamf1lualib/db    teamf1lualib/util    teamf1lualib/validations    teamf1lualib/auth_validations    teamf1lualib/returnCodes    teamf1lualib/auth_returnCodes    com.teamf1.core.returnCodes    com.teamf1.core.validations !   com.teamf1.core.auth_returnCodes 
   pop3Table    POPProfiles    pop3CATable    POPCAFiles    serverCheck 
   attribute    feature    profile    ProfileName    primaryServer    Server    primaryPort    AuthenticationPort    primarySSL 
   SSLEnable    primaryCAFile    CAFile    secondaryServer    SecondServer    secondaryPort    SecondAuthenticationPort    secondarySSL    SecondSSLEnable    secondaryCAFile    SecondCAFile    tertiaryServer    ThirdServer    tertiaryPort    ThirdAuthenticationPort    tertiarySSL    ThirdSSLEnable    tertiaryCAFile    ThirdCAFile    timeout    Timeout    retries    Retries    cafiles 	   authType 	   checkNow    updateFromWeb 	   response    primaryServerStatus    firstServerStatus    secondaryServerStatus    secondServerStatus    tertiaryServerStatus    thirdServerStatus    MAX_CERT_FILE_SIZE_LIMIT     .A   NIL    FALSE    1    0       `@              ð@      ð?      >@     ào@   _ROWID_       "@     8@   2    3    edit    Radius    pop3 	   ntDomain    ldap    activeDirectory    isfeatureEnabled    isfeatureEnabledNext    featureEnable    featureDisable    profileGet    profileGetNext    profileSet    primaryServerGet    primaryServerGetNext    primaryServerSet    primaryPortGet    primaryPortGetNext    primaryPortSet    isprimarySSLEnabled    isprimarySSLEnabledNext    primarySSLEnable    primarySSLDisable    primaryCAFileGet    primaryCAFileGetNext    primaryCAFileSet    secondaryServerGet    secondaryServerGetNext    secondaryServerSet    secondaryPortGet    secondaryPortGetNext    secondaryPortSet    issecondarySSLEnabled    issecondarySSLEnabledNext    secondarySSLEnable    secondarySSLDisable    secondaryCAFileGet    secondaryCAFileGetNext    secondaryCAFileSet    tertiaryServerGet    tertiaryServerGetNext    tertiaryServerSet    tertiaryPortGet    tertiaryPortGetNext    tertiaryPortSet    istertiarySSLEnabled    istertiarySSLEnabledNext    tertiarySSLEnable    tertiarySSLDisable    tertiaryCAFileGet    tertiaryCAFileGetNext    tertiaryCAFileSet 
   serverGet    serverGetNext 
   serverSet    serverCreate    serverDelete    pop3CAFilesGetAll    caFileDelete    caDeleteAll    caPopFileUpload    checkPop3Server    serverCheckConfig    serverCheckReset    snmp_caPopFileUpload ;                      @           NOT_SUPPORTED                     ¢   §       D   F À ^          NOT_SUPPORTED                     ·   ¼       D   F À ^          NOT_SUPPORTED                     É   Î       D   F À ^          NOT_SUPPORTED                     Ü   é           @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    profile    NIL    FAILURE    SUCCESS                     ú   ÿ       D   F À ^          NOT_SUPPORTED                       2   2      Ä      EA  À  @W     Á      A A A@  D X  D@ D FÁ^ EÁ FÂA  Ä   EB FÂ \ Á  À  ÁBÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    string    len    db    setAttribute 
   attribute    profile    FAILURE                     @  M          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    primaryServer    NIL    FAILURE    SUCCESS                     ^  c      D   F À ^          NOT_SUPPORTED                     s     9      Ä      EA  À  @W     Á      A  AAD D FÁ \  @W @W  A Á BÅA    D B BÀ  ÅÁ  ÀÀ Ä ÆÁÂ ÞÄ ÆÀ Þ        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    ipAddressCheck 
   fqdnCheck    db    setAttribute 
   attribute    primaryServer    FAILURE                     ¥  ²          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    primaryPort    NIL    FAILURE    SUCCESS                     Ã  È      D   F À ^          NOT_SUPPORTED                     Ø  ú   1      Ä      EA  À  @W     Á      A A @  D X@ D  D FÁ^ E FÁÁA  Ä   E FBÂ \ Á  À  BÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT 	   tonumber    db    setAttribute 
   attribute    primaryPort    FAILURE                                 @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    primarySSL    NIL    FAILURE    SUCCESS                     %  *      D   F À ^          NOT_SUPPORTED                     :  H      E   @   À D   FÀ    ^ D   FÀÀ    ^         status    NIL    FAILURE    SUCCESS                     U  e      E   F@À   Ä    EÁ  FÁ \ @  À  AÀ     ÀAÀ            db    setAttribute 
   pop3Table 
   attribute    primarySSL    NIL    FAILURE    SUCCESS                     s            @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    primaryCAFile    NIL    FAILURE    SUCCESS                             D   F À ^          NOT_SUPPORTED                     ¦  Ê   2      Ä      EA  À  @W     Á      A A A@  D X  D@ D FÁ^ EÁ FÂA  Ä   EB FÂ \ Á  À  ÁBÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    string    len    db    setAttribute 
   attribute    primaryCAFile    FAILURE                     Ø  å          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    secondaryServer    NIL    FAILURE    SUCCESS                     ö  û      D   F À ^          NOT_SUPPORTED                       0   9      Ä      EA  À  @W     Á      A  AAD D FÁ \  @W @W  A Á BÅA    D B BÀ  ÅÁ  ÀÀ Ä ÆÁÂ ÞÄ ÆÀ Þ        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    ipAddressCheck 
   fqdnCheck    db    setAttribute 
   attribute    secondaryServer    FAILURE                     >  K          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    secondaryPort    NIL    FAILURE    SUCCESS                     \  a      D   F À ^          NOT_SUPPORTED                     q     1      Ä      EA  À  @W     Á      A A @  D X@ D  D FÁ^ E FÁÁA  Ä   E FBÂ \ Á  À  BÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT 	   tonumber    db    setAttribute 
   attribute    secondaryPort    FAILURE                        ­          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    secondarySSL    NIL    FAILURE    SUCCESS                     ½  Â      D   F À ^          NOT_SUPPORTED                     Ò  æ   	   E      À   A  \À Ä  ÆÀWÀ   ^  ÅÀ  Æ ÁA  D   ÅA ÆÁÜ Á  À  B@  @@   	      cookieValidate 
   pop3Table    SUCCESS    db    setAttribute 
   attribute    secondarySSL    NIL    FAILURE                     ó        E   F@À   Ä    EÁ  FÁ \ @  À  AÀ     ÀAÀ            db    setAttribute 
   pop3Table 
   attribute    secondarySSL    NIL    FAILURE    SUCCESS                                 @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    secondaryCAFile    NIL    FAILURE    SUCCESS                     /  4      D   F À ^          NOT_SUPPORTED                     D  h   2      Ä      EA  À  @W     Á      A A A@  D X  D@ D FÁ^ EÁ FÂA  Ä   EB FÂ \ Á  À  ÁBÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    string    len    db    setAttribute 
   attribute    secondaryCAFile    FAILURE                     v            @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    tertiaryServer    NIL    FAILURE    SUCCESS                             D   F À ^          NOT_SUPPORTED                     ©  Î   9      Ä      EA  À  @W     Á      A  AAD D FÁ \  @W @W  A Á BÅA    D B BÀ  ÅÁ  ÀÀ Ä ÆÁÂ ÞÄ ÆÀ Þ        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    ipAddressCheck 
   fqdnCheck    db    setAttribute 
   attribute    tertiaryServer    FAILURE                     Ü  é          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    tertiaryPort    NIL    FAILURE    SUCCESS                     ú  ÿ      D   F À ^          NOT_SUPPORTED                       1   1      Ä      EA  À  @W     Á      A A @  D X@ D  D FÁ^ E FÁÁA  Ä   E FBÂ \ Á  À  BÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT 	   tonumber    db    setAttribute 
   attribute    tertiaryPort    FAILURE                     ?  L          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    tertiarySSL    NIL    FAILURE    SUCCESS                     \  a      D   F À ^          NOT_SUPPORTED                     q        E   F@À   Ä    EÁ  FÁ \ @  À  AÀ     ÀAÀ            db    setAttribute 
   pop3Table 
   attribute    tertiarySSL    NIL    FAILURE    SUCCESS                             E   F@À   Ä    EÁ  FÁ \ @  À  AÀ     ÀAÀ            db    setAttribute 
   pop3Table 
   attribute    tertiarySSL    NIL    FAILURE    SUCCESS                     ¬  ¹          @@ E     Ä  Á  AE@ @   D  FÁ ^  D  FÀÁ   À   ^          db    getAttribute 
   pop3Table 
   attribute    tertiaryCAFile    NIL    FAILURE    SUCCESS                     Ê  Ï      D   F À ^          NOT_SUPPORTED                     ß     2      Ä      EA  À  @W     Á      A A A@  D X  D@ D FÁ^ EÁ FÂA  Ä   EB FÂ \ Á  À  ÁBÀ @À        cookieValidate 
   pop3Table    SUCCESS    NIL    INVALID_ARGUMENT    string    len    db    setAttribute 
   attribute    tertiaryCAFile    FAILURE                        =    k      @@ E     Ä   EÀ  @   D  F Á ^  D  F@Á   Å   EÁ FÂÕ@ÆÀ    A Á AB E   ÅÁ ÆÂUÁFA   Á Â ÂB Å   EÂ FÃÕAÆÁ   A Â BC E   ÅÂ ÆÃUÂFB   Á Ã ÃC Å   EÃ FÄÕBÆÂ   A Ã CD E   ÅÃ ÆÄUÃFC   Á Ä ÄD Å   EÄ FÅÕCÆÃ   A Ä DE	 E   ÅÄ ÆÅ	UÄFD ^  	        db    getRow 
   pop3Table    NIL    FAILURE    SUCCESS    . 
   attribute    profile    primaryServer    primaryPort    primarySSL    primaryCAFile    secondaryServer    secondaryPort    secondarySSL    secondaryCAFile    tertiaryServer    tertiaryPort    tertiarySSL    tertiaryCAFile    timeout    retries                     ]  b      D   F À ^          NOT_SUPPORTED                          ã    W  @ @À    @ Ä  A@  D X  D @ D  FDÁ^ E  W@ÀW@@@DFÁ À \ÄA	À  ÄÆÂ	WÀÄÆÂ	WÀ	 Ä  ÆDÂ	Þ Å  WÀ@ @À Ä  ÆÂ	Þ ÅÄ  Ü  X 	 À
   C
   W @ @@   EC
 ÅC
@    DFÂ
W@
   D
   À  W @ @À   ED
   W W@À Å  A
@ D X 
 D @
 D  FÄ
^      AA  E  W@ÀW@@@DFÁ À \ÄA	À  ÄÆÂ	WÀÄÆÂ	WÀ	 Ä  ÆÄÄ	Þ Å  WÀ@ @À Ä  ÆÅ	Þ ÅÄ  Ü  X 	 À
   EE
   W @ @@   E
 ÅC
@    DFÂ
W@
   ÅE
   À  W @ @À   F
   W W@À Å  A
@ D X 
 D @
 D  FEÆ
^      AB  E  W@ÀW@@@DFÁ À \ÄA	À  ÄÆÂ	WÀÄÆÂ	WÀ	 Ä  ÆÆ	Þ Å  WÀ@ @À Ä  ÆÄÆ	Þ ÅÄ  Ü  X 	 À
   G
   W @ @@   EG
 ÅC
@    DFÂ
W@
   G
   À  W @ @À   ÅG
   W W@À Å  A
@ D X 
 D @
 D  FÈ
^      AC  E  W@@W@@ÀEÄ  \ X  @	   DH	 E  W@@W@ÀÀEÄ \ X  @	   H	 J  Ä Á	 E	 I
	ID 	Ä Á	 E	 ÅI
	I 	Ä Á	 E	 J
	IÄ 	Ä Á	 E	 EJ
	I	Ä Á	 E	 J
	ID	Ä Á	 E	 ÅJ
	I	Ä Á	 E	 K
	IÄ	Ä Á	 E	 EK
	I	Ä Á	 E	 K
	ID	Ä Á	 E	 ÅK
	I	Ä Á	 E	 L
	IÄ	Ä Á	 E	 EL
	I	Ä Á	 E	 L
	ID	Ä Á	 E	 ÅL
	I	Ä Á	 E	 M
	IÄ	D Ä EÅ Ä  
DFÂ
W@	E FÅÍ
Å À\ 
DFÂ
@	E FÎ
Å À \  
E  @
À DFEÎ
	^DFÂ
	^  :      NIL        POP3_SERVER_PROFILE_NIL    string    len    POP3_SERVER_PROFILE_INVALID    ipAddressCheck 
   fqdnCheck    SUCCESS &   POP3_SERVER_PRIMARY_IPADDRESS_INVALID    POP3_SERVER_PRIMARY_PORT_NIL 	   tonumber !   POP3_SERVER_PRIMARY_PORT_INVALID    POP3_SERVER_PRIMARY_SSL_NIL    valid 
   isBoolean     POP3_SERVER_PRIMARY_SSL_INVALID    POP3_SERVER_PRIMARY_CAFILE_NIL #   POP3_SERVER_PRIMARY_CAFILE_INVALID %   POP3_SERVER_SECONDARY_SERVER_INVALID    POP3_SERVER_SECONDARY_PORT_NIL #   POP3_SERVER_SECONDARY_PORT_INVALID    POP3_SERVER_SECONDARY_SSL_NIL "   POP3_SERVER_SECONDARY_SSL_INVALID !   POP3_SERVER_SECONDARY_CAFILE_NIL %   POP3_SERVER_SECONDARY_CAFILE_INVALID    POP3_SERVER_TERTIARY_INVALID    POP3_SERVER_TERTIARY_PORT_NIL "   POP3_SERVER_TERTIARY_PORT_INVALID    POP3_SERVER_TERTIARY_SSL_NIL !   POP3_SERVER_TERTIARY_SSL_INVALID     POP3_SERVER_TERTIARY_CAFILE_NIL $   POP3_SERVER_TERTIARY_CAFILE_INVALID    POP3_TIMEOUT_INVALID    POP3_RETRIES_INVALID 
   pop3Table    . 
   attribute    profile    primaryServer    primaryPort    primarySSL    primaryCAFile    secondaryServer    secondaryPort    secondarySSL    secondaryCAFile    tertiaryServer    tertiaryPort    tertiarySSL    tertiaryCAFile    timeout    retries    cookieValidate    db    insert    update    FAILURE                       ¤      Ä  ÆÀÞ         NOT_SUPPORTED                     °  µ      D   F À ^          NOT_SUPPORTED                     Á  Ô       E   F@À   ÁÀ    A  ÕA A@   À EÁ  \   D  FAÂ^ D  FÂ ^     
   attribute    cafiles    pop3CATable    SELECT _ROWID_,     from     db 	   getTable    next    NIL    FAILURE    SUCCESS                     á     %T   E   @   D   F@À ^  E    À   Á  \À Ä   Æ ÁWÀ   ^  ÅÀ  	  À @  À @  À @  À @  
E E D  FÁ
@
  EB
EÅ   À  ÆBÅ Å W@
@Å @
@  C Å @
 W C  EC
  C
@ À  E  @
 D  FÅÃ
^ D  FÁ
 ^        NIL    INVALID_ARGUMENT    cookieValidate    pop3CATable    SUCCESS    returnCode 
   serverGet    keyName    db    getAttribute 
   attribute    cafiles        POP3_CAFILE_USED 
   deleteRow    FAILURE                       I    #H   E       @  À @  À @  À @  
À  
 	D  D  Ä  ÆÄÀ	À	À DA	Å   Å   	Ü@ ÆAE   À  GB   WÀ ÀÀ @ BÀ À  WB  ÆB á  Àù C	À  ÅD À	 Ä  ÆÃ	Þ Ä  ÆÄÀ	Þ         pop3CATable    returnCode 
   serverGet    SUCCESS    db 	   getTable    pairs    getAttribute 
   attribute    cafiles        POP3_CAFILE_USED    deleteAllRows    NIL    FAILURE                     U  y   U   Å   WÀ   Å   À  Ä   Æ@ÀÞ  Å    Ü ÀÀÅ  Æ@Á AÁ  À  ÁÜ@ Ä   Æ@Â Þ Å  Æ@ÁÁ AÁ  À ÁÜ@ Ã  AAAA Á Á    A  U À  
  	AÚ   E FAÄ ÁÁ   A \W@ÅÀ EÁ   @ À  @ ÁEÁ   À  Ú    D  FÆ ^À D  FAÂ ^        NIL    INVALID_ARGUMENT 	   tonumber     .A   util    runShellCmd    rm -fr         /tmp/    FAILURE            rm -rf    /flash/tmp/caFiles/    mv     /flash/tmp/caFiles/    POPCAFiles.CAFile    db    getAttribute    POPCAFiles    CAFile    rowid     update    insert    SUCCESS                                 @@ E     Ä   EÀ  @   D  F Á ^  D F@Á    ^         db    getRow    serverCheck    NIL    SERVERCHECK_STATUS_GET_FAILED    SUCCESS                       Å   l    @     @@    W    W  À W     W  @ W      @   À     À@    W      A     Å@  EÁ FÂÕ@ Å@  EÁ FAÂÕ@  Å@  EÁ FÂÕ@ Å@  EÁ FÁÂÕ@  Å@  EÁ FÃÕ@ Å@  EÁ FAÃÕ@  Å ÆÀÃA EÁ FÄ  ÄÜA    D  ÁDEA  À EA @ D FÄ^ D FÅ^            SERVERCHECK_AUTH_TYPE_NIL    SERVERCHECK_AUTH_TYPE_INVALID    SERVERCHECK_OPERATION_NIL    SERVERCHECK_OPERATION_INVALID    serverCheck    . 
   attribute 	   checkNow 	   response    updateFromWeb    primaryServerStatus    secondaryServerStatus    tertiaryServerStatus    db    getAttribute 	   authType    NIL    FAILURE    update    SUCCESS                     Ñ  ñ   a    @  D   F@À ^  D  W@  D  W@  ÀD W@   D  W@  @D W@   D   FÀ ^  J   À  Á  A A Ä  IÀ À  Á  A ÁA Ä  IÀ À  Á  A B Ä  IÀ À  Á  A AB Ä IÀ À  Á  A B Ä  IÀ À  Á  A ÁB Ä IÀ   @CÅÀ  A C@   ÅÀ À  Ä Æ ÄÞ  Å  Æ@ÄÁ  @  Ü Á   D D@             SERVERCHECK_AUTH_TYPE_NIL    SERVERCHECK_AUTH_TYPE_INVALID    serverCheck    . 
   attribute 	   checkNow 	   response    updateFromWeb    primaryServerStatus    secondaryServerStatus    tertiaryServerStatus    db    getAttribute 	   authType    NIL    FAILURE    update    SUCCESS                     ó  %	   r            @@    Å  ÆÀÀ @  A À   @ AÜ      ÅÀ Æ ÂA @  AA ÜÁÂ KAÃ\A E  \ Á @ÀE  FÁÀ Á B @  A\A D  FAÄ ^E  FÁÀÁ Á  @  A\A C  Á@ÁA  AB   Á    Õ @   Z  Å ÆAÆ AÂ   Á ÜW@ÇÀ GA  À @ @ ÂGA  @ Z   Ä  ÆÈ Þ Ä  ÆAÄ ÞÀ Ä   Æ@Ä Þ   !      NIL    INVALID_ARGUMENT    util    runShellCmd 
   tftp -gr  
    -l /tmp/         io    open    /tmp/    r    seek    end    close 	   tonumber    MAX_CERT_FILE_SIZE_LIMIT    rm -fr    FAILURE            rm -rf    /flash/tmp/caFiles/    mv     /flash/tmp/caFiles/    POPCAFiles.CAFile    db    getAttribute    POPCAFiles    CAFile    rowid     update    insert    SUCCESS                             