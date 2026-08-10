return {
	-- https://github.com/codethread/qmk.nvim
	{
		"codethread/qmk.nvim",
		lazy = false,
		opts = {
			name = "Unused",
			variant = "zmk",
			-- layout = { { "x", "x" } },
			layout = {
				"_ x x x x x _ x x x x x",
				"_ x x x x x _ x x x x x",
				"_ x x x x x _ x x x x x",
				"_ _ _ x x x _ x x x _ _",
			},
		},
		-- config = function()
		-- 	---@type qmk.UserConfig
		-- 	local conf = {
		-- 		name = "Unused",
		-- 		variant = "zmk",
		-- 		-- layout = { { "x", "x" } },
		-- 		layout = {
		-- 		    '_ x x x x x x _ x x x x x x',
		-- 		    '_ x x x x x x _ x x x x x x',
		-- 		    '_ x x x x x x _ x x x x x x',
		-- 		    '_ x x x x x x _ x x x x x x',
		-- 		    '_ x x x x x x _ x x x x x x',
		-- 		},
		-- 	}
		-- 	require("qmk").setup(conf)
		-- end,
	},
}
