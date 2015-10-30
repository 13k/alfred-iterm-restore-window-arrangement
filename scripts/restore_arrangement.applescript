on alfred_script(q)

	tell application "iTerm" to activate

	tell application "System Events"
		tell process "iTerm2"
			tell menu bar 1
				tell menu bar item "Window"
					tell menu "Window"
						tell menu item "Restore Window Arrangement"
							tell menu "Restore Window Arrangement"
								click menu item q
							end tell
						end tell
					end tell
				end tell
			end tell

			activate
		end tell
	end tell

end alfred_script
