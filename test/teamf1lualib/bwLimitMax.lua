LuaQ                     A@  @    A�  @ �   A E@ F�� @ �  B B � @  ���  ��B��  ����A �A �A �  �ƀC��   ��� 7���  ��B�  ����A �A �A � 4�F@D��  Ƃ�� A �� �� ܂��  �BAC �� �� � ���C C EC @.�� FW@�@ ��� ��� ��E �D ��G	��  ��\�  �D�� ���� �� �D  �� ��	E	 �D � E �G
A� � �܄  E�	�� ��E ���	� \E  �
  ��#��C
��E�  F��
��	 � 
 AF
 \E����J
��E�  F��
��	 � 
 A�
 \E� � K
��E�  F��
��	 � 
 AF \E�E�  F��
�� � � A� \E�E� F�
� \E E�  F��
�� � � A� \E���ED FD��� ��   A �D	\� �D�E ���   	����D �� ��M	�   AE ��    	��  ��B	��	  ����� �D ń ���F�NO@�  � �  �����  ƅ��	 A �� �  �E���  ƅ�� A �� �� �E��� �� �E ��  ƅ�� A �� �� �E�@��� ��    � ���  ƅ��	 A �
 �  �E���  ƅ�� A �� �� �E��� �� �E ��  ƅ�� A �� �� �E���  ��!�  ����   ��� �I�� �A �� � @      require    teamf1lualib/util    teamf1lualib/db    db    connect    arg       �?   util    setDebugStatus    ret    getRowsWhere    BandWidthProfileStatus    rowId != 0    pairs    BandWidthProfileStatus.Status    1    BandWidthProfile    BandWidthProfile.WANID    getAttribute 	   unitName    _ROWID_    networkInterface    LogicalIfName == '    '    networkInterface.interfaceName    RVS5000 	   WRVS5000    WAN2    assert    io    open    /tmp/portSpeed.4    r    read    close    os    execute (   switchConfig /dev/bcm53980 duplex get 4    setAttributeWhere    BandWidthProfileSpeed 
   Wan2Speed    10Mb/s    2    100Mb/s    3 	   1000Mb/s    Status            sleep 1    popen    /pfrm2.0/bin/ethtool         |grep Speed | awk '{print $2}'    *a    string    gsub    
        table     BandWidthProfileSpeed.Wan1Speed     BandWidthProfileSpeed.Wan2Speed    WAN1 
   Wan1Speed    sleep 3                 