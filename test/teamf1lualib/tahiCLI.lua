LuaQ                '   $      $@  @  $    $Ŕ  Ŕ  $    $@ @ $  $Ŕ Ŕ $    $@ @ $  $Ŕ Ŕ $    $@ @ $  $Ŕ Ŕ $    $@ @ $       
   modeCheck    tahiDefaultRouteAdd    tahiDefaultRouteDel    tahiStopRA    tahiStartRA    tahiProcSet    v6UpGlobal    tahiAliasAdd    tahiAliasDel    tahiNeighCacheDel    tahiReachableTimeSet    tahiMcastStart    tahiMcastStop 
   tahiPing6    tahiRouteAdd    tahiRouteDel    tahiPmtuRouteAdd    firewall6Disable 
   lanIpShow                       @@ A  Ŕ  Á  A WA  EŔ   \@ B   ^  B  ^    	      db    getAttribute    networkInfo    _ROWID_       đ?   netWorkMode    3    printCLIError     Please Set IP Mode to IPv4/IPv6                                E   \ @Ŕ     E  \@ EŔ  F Á @ Ŕ     \      
   modeCheck     tahiDefaultRouteDel    os    execute    route -A inet6 add default gw  
    dev bdg1                              
       @@       Ŕ@ A        
   modeCheck     os    execute    ip -6 route del default                        #      
       @@       Ŕ@ A        
   modeCheck     os    execute    killall radvd 2>/dev/null                     &   ,        E   \ @Ŕ     E  \@ EŔ  F Á @ Ŕ   Ŕ \      
   modeCheck     tahiStopRA    os    execute 
   radvd -C                      /   ;        E   \ @Ŕ     @  EŔ  F Á @ \ Ŕ   AÁ  @ŔA ŔEŔ  F Á   \ Ŕ   AÁ@    
   
   modeCheck             os    execute 3   echo "1">/proc/sys/net/ipv6/conf/bdg1/disable_ipv6 3   echo "1">/proc/sys/net/ipv6/conf/eth1/disable_ipv6       đ?3   echo "0">/proc/sys/net/ipv6/conf/bdg1/disable_ipv6 3   echo "0">/proc/sys/net/ipv6/conf/eth1/disable_ipv6                     >   G             @@       AŔ  @   E@ FÁ Ŕ Ŕ   \ Â Ĺ@ ĆÂÁ @ AÜ      
   modeCheck     tahiProcSet       đ?)   LogicalIfName='LAN' and AddressFamily=10    db    getRowWhere 	   ifStatic    ifStatic.StaticIp    os    execute    ifconfig bdg1 add                      J   O            @@      Ŕ@Á    AA   Á ŐŔ      
   modeCheck     os    execute 
   ifconfig      add     /64                     R   W            @@      Ŕ@Á    AA   Á ŐŔ      
   modeCheck     os    execute    ifconfig       del     /64                     Z   _      
       @@       Ŕ@ A        
   modeCheck     os    execute    ip -6 neigh flush all                     b   g        E   \ @Ŕ     E  FŔŔ   Ŕ   A  \      
   modeCheck     os    execute    echo  5    > /proc/sys/net/ipv6/neigh/bdg1/base_reachable_time                     j   t             @@       Ŕ@ A  @ KA ÁŔ \@KA Á  \@KA Á@ \@KB \@ EŔ F Ă @ \      
   modeCheck     io    open    /var/mfc.conf    w    write @   ff1e::1:2 from 3ffe:501:ffff:100:200:ff:fe00:100@bdg1 to eth1;
 @   ff1f::1:2 from 3ffe:501:ffff:100:200:ff:fe00:100@bdg1 to eth1;
 3   ff1e::1:2 from 3ffe:501:ffff:100::1@bdg1 to eth1;
    close    os    execute    mfc /var/mfc.conf &                     w   }             @@       Ŕ@ A   E  FŔŔ @ \      
   modeCheck     os    execute    killall mfc 2>/dev/null    rm -f /var/mfc.conf                                    @@      Ŕ@Á    AA   Ő Ĺ   Ü@      
   modeCheck     os    execute 
   ping6 -s      -c 1 -I bdg1     printCLIError                                    @@      Ŕ@Á     AA  Á ŐŔ      
   modeCheck     os    execute    route -A inet6 add     /64 gw  
    dev bdg1                                    @@      Ŕ@Á     AA  Á ŐŔ      
   modeCheck     os    execute    route -A inet6 del     /64 gw  
    dev bdg1                                E   \ @Ŕ     E  FŔŔ   Ŕ   A  \      
   modeCheck     os    execute    route -A inet6 add  
    dev bdg1                     Ą   Ź             @@       Ŕ@ A  @    @ KA \@ EŔ F Â @ \ Ŕ  BÁ  ĹŔ Ć ÂÁ Ü      
   modeCheck     io    open    /var/fwIpv6LogoCheck    w    close    os    execute *   /pfrm2.0/bin/ip6tables -I INPUT -j ACCEPT ,   /pfrm2.0/bin/ip6tables -I FORWARD -j ACCEPT [   /pfrm2.0/bin/ip6tables -t raw -A PREROUTING -p icmpv6 -i bdg1 -m frag --fragres -j NOTRACK                     Ž   Á      &       @@       AŔ    @AÁ   ÁŔ    @ @  @B F ĆÂĂ FĂŐ@ W  ÁB ŐŔ!   ü @A      
   modeCheck          /   LogicalIfName = 'LAN' AND addressFamily = '10'    db    getRowsWhere    ipAddressTable        pairs       đ?   ipAddressTable.ipAddress    /    ipAddressTable.ipv6PrefixLen    ,     printCLIError                             