LuaQ                Ì      A@    À@@  A@ @   A @   AÀ @   A  @   A@ @   A  E  À \   Á   Á Ç@ Á  ÇÀ Á  Ç@ Á Ç Á  ÇÀ Á Ç@ Á  ÇÀ Á Ç@ ÁÀ Ç Á@ Ç  Ê   Ç Å É ÈÅ ÉÃÅ ÉÀHÅ É@IÅ ÉÀIÅ É@JÅ ÉJÅ É ËÅ ÉËÅ É ÌÅ ÉÌÅ É Íä       Ç@ ä@      Ç ä      ÇÀ äÀ      Ç  ä      Ç@ ä@     Ç ä        ÇÀ äÀ     Ç  ä      Ç@ ä@           Ç ä     ÇÀ äÀ     Ç  ä         Ç@ ä@     Ç ä     ÇÀ äÀ        Ç  ä      Ç@ ä@     Ç ä     ÇÀ äÀ     Ç  ä      Ç@ ä@        Ç ä     ÇÀ äÀ     Ç  ä      Ç@ ä@     Ç ä     ÇÀ äÀ     Ç  ä      Ç@ ä@     Ç ä     ÇÀ äÀ     Ç  ä      Ç@ ä@     Ç ä     ÇÀ äÀ           Ç  ä 	     Ç@ ä@	     Ç ä	     ÇÀ äÀ	     Ç    ]      module    com.teamf1.core.services.ddns    package    seeall    require    teamf1lualib/db    teamf1lualib/util    teamf1lualib/validations    teamf1lualib/returnCodes    teamf1lualib/ddns_returnCodes    com.teamf1.core.returnCodes    com.teamf1.core.validations !   com.teamf1.core.ddns.returnCodes    ENABLE    1    DISABLE    0    SERVICE_NONE    SERVICE_DDNS    SERVICE_DLINKDNS    3    SERVICE_ORAY    4    OPTION2    2    OPTION1 
   ddnsTable    ddns    ddnsStatusTable    ddnsStatus 
   attribute    key    _ROWID_ 	   keyvalue    wanPort    interfaceName    service    ddnsService    domainName 	   hostname 	   userName 	   username 	   password 	   userType 	   orayType    server    orayDomain    status    Status 
   wildCards 	   wildflag    periodicUpdate    timePeriod    wanPortGet    wanPortGetNext    wanPortSet    wanPortDelete    serviceGet    serviceGetNext    serviceSet 
   serverGet    serverGetNext 
   serverSet    userNameGet    userNameGetNext    userNameSet    passwordGet    passwordGetNext    passwordSet    userTypeGet    userTypeGetNext    userTypeSet    domainNameGet    domainNameGetNext    domainNameSet 
   statusGet    statusGetNext 
   statusSet    iswildCardsEnabled    iswildCardsEnabledNext    wildCardsEnable    wildCardsDisable    isperiodicUpdateEnabled    isperiodicUpdateEnabledNext    periodicUpdateEnable    periodicUpdateDisable    ddnsConfigGet    ddnsConfigGetNext    ddnsConfigSet    ddnsConfigCreate    ddnsConfigDelete    ddnsOption2GetAll    ddnsOption1GetAll (       S   a           @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key    wanPort    NIL    FAILURE    SUCCESS       ð?                    q       1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á    Å@ \    @     A  À  ÀAÅ@  AB@  BÄ   Æ ÀÀ À Ä   ÆÀÂ  Þ Ä   Æ Ã  @ Þ          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute 
   attribute    key    wanPort    FAILURE    SUCCESS                                    @À            NOT_SUPPORTED                     ­   ±           @À            NOT_SUPPORTED                     ¿   Í           @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key    service    NIL    FAILURE    SUCCESS       ð?                    Ý   ÷    1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á    Å@ \    @     A  À  ÀAÅ@  AB@  BÄ   Æ ÀÀ À Ä   ÆÀÂ  Þ Ä   Æ Ã  @ Þ          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute 
   attribute    key    service    FAILURE    SUCCESS                       )   G       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @      @    @B   W ÀÀ W    W @@ W    @B  À  CÅ@  ÁA@   ÁCÀ  Ä   Æ ÀÀ À Ä   Æ Ä   Þ Ä   Æ@Ä   Þ         NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     SERVICE_INVALID    SERVICE_DDNS    SERVICE_ORAY    SERVICE_DLINKDNS    SERVICE_NONE    setAttribute    service    FAILURE    SUCCESS                     7  E          @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0    ddnsStatusTable    getAttribute 
   attribute    key    server    NIL    FAILURE    SUCCESS       ð?                    U  r   1       @W  @  À    Ä   Æ ÀÀ     @  À   AÀ   A Ä   Æ ÀÀ  Ä   ÆÁÞ  ÅÀ  ÆÀÁ EA FÂ ÅA ÆÁÂÜ  @ À   C@   AC@          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute    ddnsStatusTable 
   attribute    key    server    FAILURE    SUCCESS                       ¥   F       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @      @    @B    ÀBÁ      Ä   Æ@ÃWÀ    @B  À  CÅ@  ÁA@   ÁCÀ  Ä   Æ ÀÀ À Ä   Æ Ä   Þ Ä   Æ@Ã   Þ         NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     SERVER_INVALID    valid    ipAddressCheck    2    SUCCESS    setAttribute    server    FAILURE                     ³  Á          @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key 	   userName    NIL    FAILURE    SUCCESS       ð?                    Ñ  ë   1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á    Å@ \    @     A  À  ÀAÅ@  AB@  BÄ   Æ ÀÀ À Ä   ÆÀÂ  Þ Ä   Æ Ã  @ Þ          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute 
   attribute    key 	   userName    FAILURE    SUCCESS                     û     	8   Ä   Æ ÀWÀ  Å@     Ü   @  Ä   ÆÀÞ  ÅÀ  Æ ÁA E FÁÁ  Ü  Â Ä   ÆÀÞ  Ä   Æ ÀÀ  Ä  Æ@ÂÞ  ÅÀ  ÆÂA E FÁÁ  Å ÆÁÂ  Ü   @ À   C@    AC@          NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     USERNAME_INVALID    setAttribute 	   userName    FAILURE    SUCCESS                     (  7          @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key 	   password    NIL    FAILURE    SUCCESS       ð?                    G  g   =       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @  À  @BÀ   A Ä   Æ ÀÀ  Ä   ÆÂÞ  ÅÀ  ÆÀÂA E FÁÁ Å ÆÃÜ  @ À   AC@   C@          NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     getNextRowId    TABLE_IS_FULL    getAttribute 	   password    FAILURE    SUCCESS                     w     	8   Ä   Æ ÀWÀ  Å@     Ü   @  Ä   ÆÀÞ  ÅÀ  Æ ÁA E FÁÁ  Ü  Â Ä   ÆÀÞ  Ä   Æ ÀÀ  Ä  Æ@ÂÞ  ÅÀ  ÆÂA E FÁÁ  Å ÆÁÂ  Ü   @ À   C@    AC@          NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     PASSWORD_INVALID    setAttribute 	   password    FAILURE    SUCCESS                     ¦  ´          @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0    ddnsStatusTable    getAttribute 
   attribute    key 	   userType    NIL    FAILURE    SUCCESS       ð?                    Ä  å   =       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @  À  @BÀ   A Ä   Æ ÀÀ  Ä   ÆÂÞ  ÅÀ  ÆÀÂA E FÁÁ Å ÆÃÜ  @ À   AC@   C@          NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow    ddnsStatusTable 
   attribute    key     getNextRowId    TABLE_IS_FULL    getAttribute 	   userType    FAILURE    SUCCESS                     õ  ù          @À            NOT_SUPPORTED                                 @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key    domainName    NIL    FAILURE    SUCCESS       ð?                    '  C   1       @W  @  À    Ä   Æ ÀÀ     @  À   AÀ   A Ä   Æ ÀÀ  Ä   ÆÁÞ  ÅÀ  ÆÀÁ EA FÂ ÅA ÆÁÂÜ  @ À   C@   AC@          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute    ddnsStatusTable 
   attribute    key    domainName    FAILURE    SUCCESS                     T  r   8       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @      @    @B  À  BÅ@  ÁA@   ÁBÀ  Ä   Æ ÀÀ À Ä   Æ Ã   Þ Ä   Æ@Ã   Þ         NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     DOMAIN_NAME_INVALID    setAttribute    domainName    FAILURE    SUCCESS                                 @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0    ddnsStatusTable    getAttribute 
   attribute    key    status    NIL    FAILURE    SUCCESS       ð?                      »   1       @W  @  À    Ä   Æ ÀÀ     @  À   AÀ   A Ä   Æ ÀÀ  Ä   ÆÁÞ  ÅÀ  ÆÀÁA E FAÂ Å ÆÂÜ  @ À   ÁB@   C@          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId    ddnsStatusTable    TABLE_IS_FULL    getAttribute 
   attribute    key    status    FAILURE    SUCCESS                     Ì  Ð          @À            NOT_SUPPORTED                     Þ  ì          @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key 
   wildCards    NIL    FAILURE    SUCCESS       ð?                    ü     1       @W  @  À    Ä   Æ ÀÀ     @  À   AÀ   A Ä   Æ ÀÀ  Ä   ÆÁÞ  ÅÀ  ÆÀÁA E FAÂ Å ÆÂÜ  @ À   ÁB@   C@          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute 
   attribute    key 
   wildCards    FAILURE    SUCCESS                     )  B   1       @W  @  À    Ä   Æ ÀÀ     @  À   AÅ@  ÁA@    B    @  À  @BÅ@  ÁA@   BÅÁ  Ä   Æ ÀÀ À Ä   Æ Ã   Þ Ä   Æ@Ã   Þ         NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     setAttribute 
   wildCards    ENABLE    FAILURE    SUCCESS                     O  f   1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á @ Å ÆÀÁ   \  Â  D   FÀ ^  EÀ  F@Â @ Å ÆÀÁ   E FÂÁ \     @ À     CÀ       @CÀ            NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     setAttribute 
   wildCards    DISABLE    FAILURE    SUCCESS                     t            @@ A  À  E   F Á À  Å@ ÆÁ   EA FÁÁ\    B     @B     BÁÀ             db    getNextRowId    0 
   ddnsTable    getAttribute 
   attribute    key    periodicUpdate    NIL    FAILURE    SUCCESS       ð?                      ®   1       @W  @  À    Ä   Æ ÀÀ     @  À   AÀ   A Ä   Æ ÀÀ  Ä   ÆÁÞ  ÅÀ  ÆÀÁA E FAÂ Å ÆÂÜ  @ À   ÁB@   C@          NIL 	   tonumber    INVALID_ARGUMENT    db    getNextRowId 
   ddnsTable    TABLE_IS_FULL    getAttribute 
   attribute    key    periodicUpdate    FAILURE    SUCCESS                     ¾  Ö   1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á @ Å ÆÀÁ   \  Â  D   FÀ ^  EÀ  F@Â @ Å ÆÀÁ   E FÂÁ \     @ À     CÀ       @CÀ            NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     setAttribute    periodicUpdate    ENABLE    FAILURE    SUCCESS                     ã  ü   1   D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á @ Å ÆÀÁ   \  Â  D   FÀ ^  EÀ  F@Â @ Å ÆÀÁ   E FÂÁ \     @ À     CÀ       @CÀ            NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     setAttribute    periodicUpdate    DISABLE    FAILURE    SUCCESS                       <    l   
   J      @@Á  Á  Å   Æ ÁÁ  EA FÁ Ü   Ä   ÆÀÁÀ   Ä   Æ ÂÞ  Ã Â  ÁB C BÆ Â  ÁB C ÃB Â  ÁB C CÆ Â  ÁB C CCF Â  ÁB C C Â  ÁB C ÃC Â  ÁB C DF   ÂAWÀ  ÂAWÀ  ÂAWÀ  ÂAWÀ  ÂAWÀ  ÂAWÀ   ÂA   B   BDÁ  @ À  @          db    getNextRowId    0 
   ddnsTable    getRow 
   attribute    key    NIL    FAILURE    .    wanPort    service    domainName 	   userName 	   password 
   wildCards    periodicUpdate    SUCCESS       ð?                    V        D   F À W@  E@     \     @  D   FÀ ^  EÀ  F Á @ Å ÆÀÁ   \  Â  D   FÀ ^  EÀ  F Á @ Å ÆÀÁ   \  Â  D   FÀ ^  EÀ  FÂ    Å@ \    @     ÀB  À   CÅ@  ÁA@  Ä   Æ ÀÀ @ Å@ Þ  Ã  EC  Å ÆÃÃUÃÆ@EC  Å ÆÄUÃAEC  Å ÆCÄUÃFBEC  Å ÆÄUÃAEC  Å ÆÃÄUÃÆAEC  Å ÆÅUÃÆBEC  Å ÆCÅUÃCD  FÀW@ÀD  FÀW@ÀD  FÀW@ÀD  FÀW@ÀD  FÀW@ÀD  FÀW@À D  FÀ@@ EC ^ D  FÅ À  @ À @ ^         NIL 	   tonumber    INVALID_ARGUMENT    db 
   existsRow 
   ddnsTable 
   attribute    key     ddnsStatusTable    getNextRowId    TABLE_IS_FULL    getRow    FAILURE    .    wanPort    service    domainName 	   userName 	   password 
   wildCards    periodicUpdate    SUCCESS                     ¨  ì      
  D  FÀW@ EB    \   @ D  FÀ^ D  FÀW@  EÂ  W@ ÀE W@  EB W@ @E W@  D FÂÁ^ E B Å ÆÂÂUÂ	BD  FÀW@@E B Å ÆÃUÂ	ÂD  FÀW@@E B Å ÆBÃUÂ	D  FÀW@@E B Å ÆÃUÂ	D  FÀW@@D FÂÃ\ ÀD  FÄW@ D  FÀ^ E B Å ÆBÄUÂ	BD  FÀW@@D FÂÃ \ ÀD  FÄW@ D  FÀ^ E B Å ÆÄUÂ	EÂ FÅ À    \   @À   BEÀ    DÀ          NIL 	   tonumber    INVALID_ARGUMENT    SERVICE_DDNS    SERVICE_ORAY    SERVICE_DLINKDNS    SERVICE_NONE    SERVICE_INVALID 
   ddnsTable    . 
   attribute    service 	   userName 	   password    domainName 
   isBoolean    SUCCESS 
   wildCards    periodicUpdate    db    update    FAILURE                         
      @ÅB          NOT_SUPPORTED    rowid                             D   F À    ^         NOT_SUPPORTED                       ,    '   
   J      @@Å  Á  AEA        A      ÀA     @@Å  Á  AEA  @     A     ÀA     @BÁ    @          db    getRow 
   ddnsTable 
   attribute    key    OPTION2    NIL    FAILURE    ddnsStatusTable    SUCCESS       ð?                    1  A    '   
   J      @@Å  Á  AEA        A      ÀA     @@Å  Á  AEA  @     A     ÀA     @BÁ    @          db    getRow 
   ddnsTable 
   attribute    key    OPTION1    NIL    FAILURE    ddnsStatusTable    SUCCESS       ð?                            