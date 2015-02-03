1. Express the meaning of the following sentences of the story in the knowledge representation language of frames.


I knelt in front of the unmoving blue robot. 

    I
        state: kneeling
        location: in front of Robot

    Knelt
        subject: I
        location: in front of Robot

    Robot
        state: unmoving
        color: blue


As if brooding, it sat on the floor in the middle of the living room.

    It
        state: sitting
        location: middle of the living room
        appearance: brooding

    Sitting
        subject: it
        location: middle of the living room
        on: floor


“The Johnsons across the street bought a new robot,” it said finally.

    Johnsons
        location: across the street
        action: Bought

    Bought
        subject: Johnsons
        object: Robot

    Robot
        condition: new

    It
        action: Said

    Said
        subject: It
        statement: Johnsons bought a new robot

“Yeah,” the husband confirmed from behind me, “One of those new A-01 models.”

    Husband
        action: confirmed
        location: behind me
        statement: Yeah, one of those new A-01 models

    Confirmed
        subject: Husband
        statement: Yeah, one of those new A-01 models

    A-01
        condition: new
        instance-of: model




  2. In this story, the protagonist performs a kind of diagnosis and repair of Henry the robot. Illustrate the production system architecture for the diagnosis task in the story. Invent percepts, actions and rules as needed (with at least 3 percepts, 3 actions, 3 rules). Demonstrate how the production system architecture would work for this story (that is, given Henry’s symptoms, it would ask the same questions that our protagonist asks). Show the evolving contents of the working memory.


Robots love me.
 
 As much as robots can love. And in a Platonic sense, of course. Something about my chubby little baby face sets off their simulated paternal instincts and they all bend over backwards to answer my questions. That sort of thing comes in handy with my job.
 
 I knelt in front of the unmoving blue robot. As if brooding, it sat on the floor in the middle of the living room. It was large and bulky, a few years old but in decent enough shape. Not one of those smooth, humanoid-looking models that have been flooding the market. It was more from the “Rock ’Em, Sock ’Em” school of design. Behind me, the family stood anxious, worried, huddled together.
 
robot name:

If: 
    robot has no name
Then: 
    say, “Unit NX-6401, respond to my voice.”

If: 
    robot responds with his name
Then: 
    set robot name

If:
    robot has name 
    problem is unknown
Then:
    say, "Are you functioning correctly"

If:
    robot has name 
    problem is unknown
    robot says, “If that’s what you call this.”
Then:
    set problem uncertain

If:
    problem is uncertain
Then:
    say, “Hey, now. What’s that all about?”


 It made a soft snorting noise. “If that’s what you call this.”

“Hey, now. What’s that all about?” I put my hand on its shoulder.

Henry’s ocular lights activated, but just barely. It didn’t respond right away.

 “The Johnsons across the street bought a new robot,” it said finally.

 “Go on,” I coaxed.

 “I’ve seen it walking their kids to school and fixing their roof, and it’s got those extendable arms and a hedge-clipper accessory, and...”

 “And its making you feel not as special?” I asked in a soothing voice.

 “The A-01s are so great,” it said. “One of them would be so much more functional for this family. It would be better than I am.”

 “Henry, I’m going to tell you a secret about humans. It is a bit paradoxical, so promise me your head will not explode when I tell you.”

 It nodded, its eyes glowing brighter. 

 “Henry,” I said. “Humans build emotional attachments. And they don’t always want what’s shiny and new. They want what they love.”

 “They love me?” it asked. It stood up, and after a moment, I followed.

 “It isn’t very logical, doctor.” Henry’s voice sounded happy.

 I smiled. “I’m not a doctor.” 


  3. Now suppose that one of the rules was missing in the long-term memory of the production system. Show why, when and how this rule may be learned from the case base. 
