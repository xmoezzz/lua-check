import matplotlib.pyplot as plt

labels = ['Lua-related', 'Not Lua-related']
counts = [213, 835 - 213]

plt.figure(figsize=(6, 6))
plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Lua-related Command Injection in IoT CVEs')
plt.axis('equal')
plt.tight_layout()
plt.savefig('lua_related_command_injection.png')
plt.show()
