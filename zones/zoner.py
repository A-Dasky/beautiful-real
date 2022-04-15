imp = 'quiet_forest'
with open(imp + '.w', 'w') as w:
    # height
    for i in range(51):
        # width
        for j in range(77):
            w.write('F')
        w.write('\n')
