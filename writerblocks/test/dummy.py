
full_text_i = """This scene is the prologue and sets the stage for the actual beginning.

##  

This is the scene where our heroes get their quest in the bar.

"Beware, young adventurers," croaked the old quest-giver. "The road you must travel is full of **peril**!"

"Why did you pronounce 'peril' that way, quest-giver?" Bob asked.

"I said '**peril**,' not 'peril,'" the old quest-giver snapped. "They're very different things!"

"But how, quest-giver?" Alice protested.

"You will learn that soon enough, young adventurer," the old quest-giver replied, and vanished into the darkness.

####  

This is the "baz" scene, in which our heroes meet the jolly rascal Baz. Note that there is no actual content in this scene yet; the file is just a placeholder because the author knows that this scene must occur.

###  

This is the "foo" scene, in which our heroes encounter the dread Foo Beast for the first time.

"Oh no!" Alice exclaimed. "Look out, Bob! It's the dread Foo Beast!"

"Crikey!" Bob replied. "I didn't know there were Foo Beasts here! We better skedaddle!"

####  

This scene is just a filler to draw out the suspense.

##  

This scene reveals the secret of Alice's backstory. I can't actually include it because it's secret!

##  

Something goes here, but it's hard to know what yet!

####  

This scene is another filler scene, but it comes later than the first one.

###  

This scene tells us something very important about Bob's backstory.

##  

This is the climactic end scene! It's very exciting and Bob dies.

##  

This is the epilogue, featuring Bob's funeral and Alice's grim life after the events of the story."""

full_tags = ("char:alice",
             "char:quest-giver",
             "char:bob",
             "filler",
             "char:alice's pet dog",
             "char:baz",
             "foo,"
             "key:alice",
             "**peril**",
             "char:carol",
             "char:hans")


full_text_a = """## Prologue 

This scene is the prologue and sets the stage for the actual beginning.

## The Beginning 

This is the scene where our heroes get their quest in the bar.

"Beware, young adventurers," croaked the old quest-giver. "The road you must travel is full of **peril**!"

"Why did you pronounce 'peril' that way, quest-giver?" Bob asked.

"I said '**peril**,' not 'peril,'" the old quest-giver snapped. "They're very different things!"

"But how, quest-giver?" Alice protested.

"You will learn that soon enough, young adventurer," the old quest-giver replied, and vanished into the darkness.

***

This is the "baz" scene, in which our heroes meet the jolly rascal Baz. Note that there is no actual content in this scene yet; the file is just a placeholder because the author knows that this scene must occur.

####  

This is the "foo" scene, in which our heroes encounter the dread Foo Beast for the first time.

"Oh no!" Alice exclaimed. "Look out, Bob! It's the dread Foo Beast!"

"Crikey!" Bob replied. "I didn't know there were Foo Beasts here! We better skedaddle!"

***

This scene is just a filler to draw out the suspense.

## The Middle 

This scene reveals the secret of Alice's backstory. I can't actually include it because it's secret!

## The Buildup 

Something goes here, but it's hard to know what yet!

***

This scene is another filler scene, but it comes later than the first one.

####  

This scene tells us something very important about Bob's backstory.

## The Climax 

This is the climactic end scene! It's very exciting and Bob dies.

## Epilogue 

This is the epilogue, featuring Bob's funeral and Alice's grim life after the events of the story."""

files_to_tags = {
    'scenes/alice_backstory.md': set("char:alice,key:alice,char:alice's pet dog".split(',')),
    'scenes/bar.md': set("char:alice,char:bob,char:quest-giver,**peril**".split(',')),
    'scenes/baz.md': set("char:alice,char:bob,char:baz".split(',')),
    'scenes/bob_backstory.md': {"char:bob"},
    'scenes/climactic_end.md': set("char:alice,char:bob,**peril**".split(',')),
    'scenes/epilogue.md': set("char:alice,char:bob".split(',')),
    'scenes/filler_1.md': set("filler,char:alice,char:bob,char:carol".split(',')),
    'scenes/filler_2.md': set("filler,char:alice,char:carol".split(',')),
    'scenes/foo.md': set("char:alice,char:bob,char:hans,foo,**peril**".split(',')),
    'scenes/prologue.md': {"char:bob"},
    'scenes/tbd.md': set(),
}

tags_to_files = {
    tag: [filename for filename in files_to_tags if tag in files_to_tags[filename]]
    for tag in full_tags
}


def get_matchsets(tag):
    full, partial, non = [], [], []
    for other in full_tags:
        if other == tag:
            continue
        if any(filename in tags_to_files[other] for filename in tags_to_files[tag]):
            if all(filename in tags_to_files[other] for filename in tags_to_files[tag]):
                full.append(other)
            else:
                partial.append(other)
        else:
            non.append(other)
    return full, partial, non


best_index_files = ['index.yaml', 'index.yml', 'index.json']
good_index_files = ['foo_index.yaml', 'bar_index.json', 'an_index_file.json']
bad_index_files = ['not_the_right_file.yaml']

all_index_files = best_index_files + good_index_files + bad_index_files
