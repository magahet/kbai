% Creating an Intelligence Analysis Assistant
% Magahet Mendiola
  (mmendiola3@mail.gatech.edu)
% March 8th, 2015
\makeatletter
\def\verbatim{\small\@verbatim \frenchspacing\@vobeyspaces \@xverbatim}
\makeatother



## Introduction

The goal of our design will be an AI agent capable of ingesting a stream of events, predict future crimes based on these events, and alert human analysts when a crime appears to be imminent. 

The intelligence system would include an analysis engine, a state data-store, and a meta-cognition process. These components would interact to use the stream of events to build a long-term understanding of not only whether someone will commit a crime, but also to learn how to recognize new ways to predict crimes. The only prerequisite would be that the system could be told whether a given event is considered a crime in itself.


## Knowledge Representation

The analysis engine would utilize a thematic-role system to represent the actions expressed in each event and the actor states as affected by those actions. This system would represent action frames directly mapped to the frames provided by the events. This includes slots for event, actor, object, location, time, and instrument. 

State frames would include pertinent slots required for the analysis engine to match against previously recorded states which eventually lead to a state in which the actor has committed a crime. For example, the following event would produce the resulting state:

    Action Frame:
    verb: Bought
    actor: TidMarsh
    object: gun
    location: Atlanta
    time: Monday
    instrument: credit-card

    State Frame:
    actor: TidMarsh
    location: Atlanta
    possessions: gun
    suspicious activity: 

These states would be stored in memory for retrieval by the analysis engine and meta-cognition process. The event stream for each actor would also need to be stored. Finally, a set of trigger states would need to be stored. These trigger frames would include the current set of state frames that best indicate that a crime is about to be committed. For example, the following would likely be included in this set:

    State Frame:
    possessions: gun
    suspicious activity: surveilled bank


## System Architecture

### Analysis Engine

To begin with, our agent will need to load event frames as they become available and pass those to the analysis engine. The analysis engine would first update the current stored state of the actor identified in the frame. In the case where there is no current state for the given actor, a new state will be create based on the information available in the event frame. 

The analysis engine would use a rules based engine to determine whether an event triggered one of the following further actions:

    R1: state in trigger state set,
    Then trigger alert to a human analyst.

    R2: event describes a crime taking place,
    Then run meta-cognition to refine trigger states.

If a trigger state is reached that indicates a potential crime may occur in the future, the analysis engine would flag all events associated with moving the actor into the current state and notify a human analyst.

If the event indicates that a crime has taken place, the meta-cognition process would be run to analyze the events that led up to the crime in an attempt to learn how the analysis engine could predict crimes given new events it encounters. This process is described in the next section.


### Meta-Cognition Process

In the event that a state is reached in which a crime has been committed, the meta-cognition process would determine which previous states would most likely indicate that the actor would reach the current state. This process would utilize incremental concept learning and/or machine learning classification to form or refine the trigger state that should be watched for by the analysis engine. The following example illustrates this process:

    State Frame:
    actor: TidMarsh
    location: Atlanta
    possessions: gun
    suspicious activity: 

Given the previous state, the meta-cognition process may see cases where actors eventually did commit a crime and others where they did not. This would, therefore, not be a considered a good trigger state. However, the following state would be a very clear indicator that a future state will be reached that includes a crime being committed:

    State Frame:
    actor: TidMarsh
    location: Atlanta
    possessions: gun
    suspicious activity: surveilled bank

The meta-cognition engine would see this commonality across the previous state chains and would therefore add or refine the trigger state that predicts bank robberies. Adding this trigger state to the agent’s memory will allow the analysis engine to alert on events that move an actor into a state that matches this one.


### Example Event Flow

Given the example stream of events, we will explore the behavior of our AI agent both before and after the “bank robbery” trigger state is learned.

    Trigger states: None

    Agent receives:
        (Bought (JaneDoe, icecream, Atlanta,
                 Tuesday, cash))

    Agent sets state:
        actor: JaneDoe
        location: Atlanta
        possessions: icecream
        suspicious behavior: None

    Agent receives:
        (Ate (JaneDoe, icecream, Atlanta,
              Tuesday, spoon))

    Agent sets state:
        actor: JaneDoe
        location: Atlanta
        possessions: None
        suspicious behavior: None

    Agent receives:
        (Videotaped (TidMarsh, bank, Atlanta,
                     Thursday, video-camera))

    Agent sets state:
        actor: TidMarsh
        location: Atlanta
        possessions: None
        suspicious behavior: surveilled bank

    Agent receives:
        (Bought (TidMarsh, gun, Atlanta,
                 Monday, credit-card))

    Agent sets state:
        actor: TidMarsh
        location: Atlanta
        possessions: gun
        suspicious behavior: surveilled bank

    Agent receives:
        (Stole (TidMarsh, car, Atlanta, Friday, …))

    Agent sets state:
        actor: TidMarsh
        location: Atlanta
        possessions: gun, car
        suspicious behavior: surveilled bank

Given that this event is itself a crime, the meta-cognition process would analyze the set of states leading up to this state. It would add a trigger that reaching the state with suspicious behavior: surveilled bank should alert an analyst. However, after running the agent long enough, a case may be seen where surveilling a bank may be innocuous behavior (possibly done for insurance or security reasons) and the trigger state would be removed.

    Agent receives:
        (Drove (JaneDoe, car, Atlanta, Tuesday, …))

    Agent sets state:
        actor: JaneDoe
        location: Atlanta
        possessions: None
        suspicious behavior: None

    Agent receives:
        (Drove (TidMarsh, car, Atlanta, Friday, …))

    Agent sets state:
        actor: TidMarsh
        location: Atlanta
        possessions: gun, car
        suspicious behavior: surveilled bank

Now suppose the agent receives the following:

    (Stole (TidMarsh, money, Atlanta, Tuesday, gun))

The agent would again run the meta-cognition process and identify a previous state to use as a new concept of a bank robbery trigger state:

    Trigger state:
        possessions: gun, car
        suspicious behavior: surveilled bank

If the same set of events were given to the system at this point, the analysis engine would flag the event when TidMarsh stole the car on Friday. This would have put that actor into the bank robbery trigger state, which would lead the agent to notify a human analyst that a bank robbery may be imminent. 


### Concept Refinement

Taking this one step further, if a similar case was recorded where a bank robbery event took place without a car, the meta-cognition process would update it’s trigger state concept to make possession of a car irrelevant and the trigger state would simply include: possessions: gun; suspicious behavior: surveilled bank. Thus, the next time a similar set of events occurs, the agent will trigger an alert even sooner, when the actor has purchased the gun after having videotaped the bank.
