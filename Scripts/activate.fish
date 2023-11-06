# This file must be used using `source bin/activate.fish` *within a running fish ( http://fishshell.com ) session*.
# Do not run it directly.

function _bashify_path -d "Converts a fish path to something bash can recognize"
    set fishy_path $argv
    set bashy_path $fishy_path[1]
    for path_part in $fishy_path[2..-1]
        set bashy_path "$bashy_path:$path_part"
    end
    echo $bashy_path
end

function _fishify_path -d "Converts a bash path to something fish can recognize"
    echo $argv | tr ':' '\n'
end

function deactivate -d 'Exit virtualenv mode and return to the normal environment.'
    
    if test -n "$_OLD_VIRTUAL_PATH"
        
        if test (echo $FISH_VERSION | head -c 1) -lt 3
            set -gx PATH (_fishify_path "$_OLD_VIRTUAL_PATH")
        else
            set -gx PATH $_OLD_VIRTUAL_PATH
        end
        set -e _OLD_VIRTUAL_PATH
    end

    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME "$_OLD_VIRTUAL_PYTHONHOME"
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
       and functions -q _old_fish_prompt
        
        set -l fish_function_path

      
        functions -e fish_prompt
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
    end

    set -e VIRTUAL_ENV

    if test "$argv[1]" != 'nondestructive'
      
        functions -e pydoc
        functions -e deactivate
        functions -e _bashify_path
        functions -e _fishify_path
    end
end


deactivate nondestructive

set -gx VIRTUAL_ENV 'C:\Users\bigmonke420\Desktop\serveris\env'


if test (echo $FISH_VERSION | head -c 1) -lt 3
   set -gx _OLD_VIRTUAL_PATH (_bashify_path $PATH)
else
    set -gx _OLD_VIRTUAL_PATH $PATH
end
set -gx PATH "$VIRTUAL_ENV"'/Scripts' $PATH


if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

function pydoc
    python -m pydoc $argv
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    
    functions -c fish_prompt _old_fish_prompt

    function fish_prompt
        
        set -l prompt (_old_fish_prompt)

       
        if test -n ''
            printf '(%s) ' ''
        else
            printf '(%s) ' (basename "$VIRTUAL_ENV")
        end

        string join -- \n $prompt # handle multi-line prompts
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
end
