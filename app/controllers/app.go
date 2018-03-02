package controllers

import (
	"github.com/revel/revel"
)

type App struct {
	*revel.Controller
}

func (c App) ProcessSentimentAnalysis(myName string) revel.Result {
	return c.Render(myName)
}

func (c App) UpdateSentimentData() revel.Result {
	data := map[string][]float32{}

	return c.Render(data)
}

func (c App) Index() revel.Result {
	return c.Render()
}
