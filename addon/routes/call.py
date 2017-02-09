import xbmc

from addon import addon
from addon import mpr
from addon import player

from addon import utils

@mpr.s_url('/call/started/')
def on_call_started(data):
    utils.log('Received call start event')

    data = utils.execute_jsonrpc('Application.GetProperties',
                                 {'properties': ['volume']})

    if data and 'volume' in data:
        volume = data['volume']
        addon.setSetting('saved_volume', str(volume))

    action = 0
    volume = 0
    if player.isPlayingAudio():
        action = int(addon.getSetting('music.on_call'))
        volume = int(addon.getSetting('music.volume'))

    elif player.isPlayingVideo():
        action = int(addon.getSetting('video.on_call'))
        volume = int(addon.getSetting('video.volume'))


    if action == 1:
        if not xbmc.getCondVisibility('Player.Muted'):
            xbmc.executebuiltin('Mute')

    elif action == 2:
        if not xbmc.getCondVisibility('Player.Paused'):
            player.pause()

    elif action == 3 and volume:
        xbmc.executebuiltin('XBMC.SetVolume(%d, showvolumebar)' % (volume))

    return True

@mpr.s_url('/call/ended/')
def on_call_ended(data):
    utils.log('Received call end event')


    reset_vol = False
    if player.isPlayingAudio():
        action = int(addon.getSetting('music.on_call'))

        unmute     = addon.getSetting('music.unmute') == 'true'
        play_after = addon.getSetting('music.play_after') == 'true'
        reset_vol  = addon.getSetting('music.reset_volume') == 'true'

    elif player.isPlayingVideo():
        action = int(addon.getSetting('video.on_call'))

        unmute     = addon.getSetting('video.unmute') == 'true'
        play_after = addon.getSetting('video.play_after') == 'true'
        reset_vol  = addon.getSetting('video.reset_volume') == 'true'


    if action == 1 and unmute:
        if xbmc.getCondVisibility('Player.Muted'):
            xbmc.executebuiltin('Mute')

    elif action == 2 and play_after:
        if xbmc.getCondVisibility('Player.Paused'):
            player.pause()

    elif action == 3 and reset_vol:
        try:
            volume = int(addon.getSetting('saved_volume'))
            xbmc.executebuiltin('XBMC.SetVolume(%d, showvolumebar)' % (volume))
        except:
            pass

    return True

@mpr.s_url('/call/missed/')
def on_call_missed(data):
    utils.log('Received call missed event')
    return True