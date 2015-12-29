# ClickTT: Click & Time Track

This repository contains a set of scripts and instructions to integrate "flic"
with "toggl". Additionally it also contains a script to migrate data from my
current time tracker app in iOS (TimeOrg).

The idea, is to hang "flic" in my company's badge lace, so that I can click it
when I start working to start reporting, and click it again when I stop working
(i.e. going for lunch, or going home), to stop the current ongoing timer. 

To time track my time I have decided to use "toggl", via a proxy service made
in python, which will be responsible of filling the gaps: toggl has a REST API,
but it requires the client to track the state.


## The Sytem in Brief
ClickTT integrates flick and toggle via a proxy service running in the web. 
The idea is described in the following graphic:

![ClickTT Overview](doc/images/clicktt-overview.png)


### flic
The description in its portal explains it very well:
   "Flic is a small wireless button that you can stick anywhere. It connects to
    your iOS or Android device and works right from the start". 

![ClickTT Overview](http://flic.io/assets/flic-with-outline-99b99c2492aaaec2cf931bb5e40ae538f0a0d2383d9736a5525c512db1abe3ea.png)

The button is paired with an iOS/Android device (in my case I will just refer
to an iOS device, since that's the phone I use), and it works by sending the
following events to the phone: ("click", "double-click", "hold-click"). 

The phone does not make anything with this clicks by default, so it is
necessary to install the Flic application, from which you can associate
different acctions to any of the triggering events mentioned above.

One of the possibilities, the flic app offers, is to send an (1) HTTP request
to a certain URL, which works perfectly for simple apps. Also, it supports the
(2) integration with IFTT (IF This then That) service, where you can plug the
triggering event to more services.

Unfortunately, IFTT (2) does not integrate toggl.com as of today, so I decided
to put the pieces together, by creating a proxy service, which will be
contacted from the Flic app using (1). The ClickTT proxy will have the hability
to retrieve the state from the toggle service, and according to it, send the
appropriate JSon message (Start/Stop) over HTTP.

You can find more about Flic in its Website: https://flic.io

### ClickTT proxy service (clickttd)
ClickTT is a python daemon that work as a man in the middle between the Flic
app and toggl. The proxy, offers a simple HTTP request interface in one side
(using some authentication mechanism), have the logic to retrive the current
status in toggl and decides whether to send a start or a stop reqeust.

For the time being, this is the idea. I will update this section later on when
the service is more mature (<<TODO>>: update)

### Toggl 
Toggle is a online time tracker, which I have choosen  because it looks neat
(haven't started to use it yet) and because it has a RESTful API (I love
lightweight webservices!).
I also like about toggl that it has integration (via extensions) with todoist,
which makes it very tempting to try out :-)

I won't say much more about toggl, but if you're interested, please check out
their website here: https://toggl.com

Check out their APIs here:
https://github.com/toggl/toggl_api_docs


## Setup
As an example on how to setup the system, I describe how I have interconnected
flic with my ClickTT proxy running on AWS cloud, and from there, how to setup
ClickTT to log in the correct account.
(<<TODO>>: complete)
