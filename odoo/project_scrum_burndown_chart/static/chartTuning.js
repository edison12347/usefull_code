openerp.project_scrum_burndown_chart = function (instance, local) {
    
    instance.web_kanban.KanbanGraphWidget.include({
        bar : function (data) {
            var self = this;
            nv.addGraph(function () {
                var chart = nv.models.discreteBarChart()
                    .x(function(d) { return d.label })    //Specify the data accessors.
                    .y(function(d) { return d.value })
                    .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
                    .tooltips(true)        //Don't show tooltips
                    .showValues(true)       //...instead, show the bar value right on top of each bar.
                    .transitionDuration(0);

                d3.select(self.svg)
                    .datum(data)
                    .call(chart);
                nv.utils.windowResize(chart.update);

        if(instance.client._current_state.model == "project.scrum.sprint"){
                    local_obj = self.$('.nv-groups');

                    let str_svg_line = `<svg><line x1="0" y1="10" x2="435" y2="83" style="stroke:rgb(255,0,0);stroke-width:2" /></svg>`;
                    local_obj.last().before(str_svg_line);
                }
                return chart;
            });
        },
    });
}