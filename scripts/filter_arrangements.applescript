on run
	set query to "{query}"

	tell application "System Events"
		tell process "iTerm"
			tell menu bar 1
				tell menu bar item "Window"
					tell menu "Window"
						tell menu item "Restore Window Arrangement"
							tell menu "Restore Window Arrangement"
								set arrangements to {}
								set allArrangements to get name of every menu item

								if (length of query) > 0 then
									repeat with arrangement in allArrangements
										if arrangement contains query
											set arrangements to (arrangements & arrangement)
										end if
									end repeat
								else
									set arrangements to allArrangements
								end if

								set xml to "<?xml version=\"1.0\"?><items>"

								repeat with arrangement in arrangements
									set xml to (xml & "<item uid=\"" & arrangement & "\" arg=\"" & arrangement & "\"><title>" & arrangement & "</title></item>")
								end repeat

								set xml to (xml & "</items>")

								copy xml to stdout
							end tell
						end tell
					end tell
				end tell
			end tell
		end tell
	end tell
end
