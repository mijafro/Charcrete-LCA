def replace_stuff(main_act, sub_act, repl_act, method):
    
    # first we need the demand of the sub_act in the main act
    for exc in list(main_act.exchanges()):
        if exc.input.id == sub_act.id:
            demand = exc['amount']
    
    gangnam_style = 1_000_000

    indices = np.array(
    [
        (gangnam_style, gangnam_style), # Production exchange for new main_act ( activity produces itself ) - need to have this to make matrix square
        (main_act.id, gangnam_style),  
        (sub_act.id, gangnam_style), # subtract sub_act
    ] + [
        (node.id, gangnam_style) for node in [repl_act] # replace with this - something about new dps replacing old ones - could also have the values being added together?
        # see gh bw processing -> policies
    ], dtype=bwp.INDICES_DTYPE
    )
    
    data = np.array([
            1,
            1,
            demand, # old activity
        ] + [
            demand # new activity - same amount
        ]
    ) 
    flip = np.array(
        [False, True, False] + [True for _ in [repl_act]] # First False because ?, True - motor is consumed, False because numbers are negative ... ?,
        # WAIT I think I get it. This is the data array, where we put False for old act, and True for new act...
        # ...This is probably where we would want to change things to create new market shares...?
    ) # could alsos set minussign if you prefer but i still wouldnt know where
    
    # return(demand)
    
    dp = bwp.create_datapackage()

    dp.add_persistent_vector(
        matrix="technosphere_matrix",
        data_array=data,
        indices_array=indices,
        flip_array=flip,
        name="New technosphere",
    )
    
    _, data_objs, _ = bd.prepare_lca_inputs({main_act: 1}, ipcc) # data_objs - still using ei
    
    lca = bc.LCA({main_act.id: 1}, data_objs=data_objs + [dp]) # old motor + add [dp] (new motor)
    lca.lci()
    lca.lcia()
    lcascore1 = lca.score # first version
    
    lca.lcia({gangnam_style: 1}) # new motor
    lcascore2 = lca.score # substituted sub_act w repl_act
    
    return(lcascore1, lcascore2)

