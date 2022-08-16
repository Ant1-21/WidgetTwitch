command: 'python3 Twitch.widget/app.py'

refreshFrequency: '10s'

update: (output, domEl) ->
    $(domEl).empty().append("#{output}")


style: """
color: black
background-color: rgba(255,255,255,0.5)
-webkit-backdrop-filter: blur(20px)
-webkit-box-shadow: 10px 10px 47px 0px rgba(0,0,0,0.54)
margin: 0px
left: 20px
top: 20px
border-radius:10px
font-family: Helvetica
font-size: 14px;

.main {
    height: 2rem; 
    width: 280px;
    margin: 15px;
}

.frame{
    display: flex; 
    width: 100%; 
    height: 100%;
}

a {
    text-decoration: none;
    color: black; 
}

.frame img {
    width: 2rem;
    height: 100%;
    border-radius: 50%;
    margin-right: 0.75rem;
}

.frame div.text {
    width: 100%; 
    height: 100%;
    display: grid;
    margin-bottom: 10px;
}

.frame div.text p {
    width: 100%;
    margin: auto 0 auto 0;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    line-height: 1rem;
}

.frame div.spec {
    margin-left: 0.5rem;
    display: flex;
    vertical-align: top;
}

.frame div.spec p {
    line-height: 1rem;
    margin: 0 0 0 auto;
    vertical-align: middle;
}

.frame div.spec p.disconnected {
    margin: auto 0 auto 0;
}

.frame div.spec p.live {
    color: red;
    font-size: 20px;
}

"""
