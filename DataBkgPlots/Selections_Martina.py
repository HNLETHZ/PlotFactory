import modules.Selections as Selections

channel = 'eem_SS'

selection_martina = Selections.Region('selection_martina',channel,'SR_Martina')

print 'channel = '+ channel 
print '#######################################################################################'
print '### selection baseline'
print '#######################################################################################'
print selection_martina.baseline

print '#######################################################################################'
print '### selection data (baseline + tight12)'
print '#######################################################################################'
print selection_martina.data

print '#######################################################################################'
print '### selection prompt MC (baseline + tight12 + prompt_extention)'
print '#######################################################################################'
print selection_martina.MC_contamination_pass

