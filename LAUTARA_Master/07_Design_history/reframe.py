from pathlib import Path
p=Path('production/build.py');s=p.read_text()
pairs=[
('Coastal planning game','Coastal monitoring workspace'),
('A coastal planning game that asks one more question: <i>how deep?</i>','A survey-planning workspace for government coastal monitoring teams'),
('Imagine a crew preparing a baseline survey before proposed sand extraction near a reef. Someone hands them a map pin. The skipper knows where to stop. The person holding the sampling cable still needs to know how far to lower it.','A coastal monitoring officer is reviewing proposed sand extraction near a reef. Before work starts, the field crew needs a baseline. A map pin tells the skipper where to stop. It leaves the crew to guess which depth to sample and why.'),
("start(2,'The innovation');title('Turn the ocean sideways')","start(2,'The internal workspace');title('Open a case. Inspect the water.')"),
('Choose a stretch of coast from above. Draw a line through the place you want to check. The camera pivots around that line, revealing the water beneath the boat while the jetty stays in sight.','Open a coastal works case, select the reef, and draw a line through the proposed station. The map tilts along that line. The boat stays in view as the officer inspects the water beneath it.'),
("p(42,595,'Product concept illustration · An imagined Indonesian waterfront and sampling boat.'","rect(51,247,237,44,cream);label(60,253,'EXAMPLE CASE  /  DRAFT SURVEY PLAN',8);label(60,267,'Kodingareng · Pre-work baseline',12,ink)\np(42,595,'Illustrative case view · The waterfront and seabed are concept artwork.'"),
('Lower it to compare current estimates at different depths. A field team can use the result to choose what to measure before work begins and save the reason for that choice.','Drag it to a model depth to see the dated current estimate. Select a second depth to compare, then add a proposed sample to the case. The officer records the reason for the request.'),
("start(3,'The player experience');title('One boat. Two bottles.')","start(3,'A day in the monitoring office');title('From a case file to a crew brief')"),
('Your mission is to find out whether conditions change with depth near the reef. You have one trip and two sampling bottles.','In this example, the field lead has one scheduled visit. The officer wants comparable sediment samples at two depths before work begins. Here is how they prepare the request.'),
('Pin a depth, then move the second bottle. Compare the two layers.','Select the two target depths. Attach the dated model view to the request.'),
('One station beside the reef. Sample near the surface and near the bed during the same visit. Record both depths and times so the crew can compare the bottles.','Field lead: collect paired surface and near-bed samples at the selected reef station before work. Log depths, times and sample IDs. Return suspended-sediment results to the case reviewer.'),
("start(5,'Features and missions');title('Play the coast twice')","start(5,'Internal review and handoff');title('What the next reviewer inherits')"),
('Give the player one choice worth revisiting. Each feature changes what the crew can learn on its next trip.','A colleague reopening the case should see the evidence available at the time, the officer’s reasoning, and the field results that came back.'),
('Two-bottle challenge','Survey design'),
('Use both bottles at one station to compare depths, or spend one at a reference station to compare places. The mission sets the question.','Compare two depths at one station or two stations at the same depth. Choose the design that answers the case question.'),
("'Rewind','Try taking a baseline before work begins. Replay with the boat held in reserve. Compare the questions each plan can still answer.'","'Plan comparison','Save a draft baseline plan alongside an alternative. A supervisor can review the differences and record which plan to issue.'"),
("'Coast Swap','Hand the same evidence rules to a reviewer on the other coast. Save where their conclusion changed and which record changed it.'","'Peer review','Indonesian and Russian teams could exchange selected case briefs, apply the same evidence rules and document disagreements.'"),
('THREE COASTS, THREE DIFFERENT MISSIONS','THREE REFERENCE CASES'),
('Recreate a published surface-and-bottom sampling design. Both teams can review the plan. Unlock measured values only after verifying the underlying records.','Use a published surface-and-bottom survey as a reference for paired sampling. Check the underlying records before attaching a measured value.'),
('Prepare a small data package for each coast in advance. The browser can then respond immediately when the player rotates the scene, lowers a bottle or rewinds a decision.','Prepare dated coastal layers in advance for fast inspection. Keep case records and review decisions in an access-controlled service. The map and case file share the selected station, depth and source.'),
('Store site, date, bottle positions and decision history as replayable state. Support dragging and keyboard depth controls.','Display the case, station, date, evidence and draft plan. Offer both the cable gesture and keyboard depth entry.'),
('Delivery and export<br/>Static hosting + browser print','Case records<br/>FastAPI + PostgreSQL'),
('Load each mission on demand. Cache its assets, save choices locally and produce a printable crew brief with the source date and sampling rationale.','Use agency sign-in and role-based access. Version survey plans, record sign-off, attach field results and export the issued brief with its evidence sources.'),
('On an ordinary laptop, drag the bottle through two real depth layers. Verify that each arrow and source label update together and that rewind restores both.','Can a colleague open an issued brief, recover its exact source and depths, and attach measured results to the correct station?'),
('Fetch data while preparing a mission.','Fetch public data when preparing the case layers.'),
]
for a,b in pairs:
 assert a in s,a
 s=s.replace(a,b)
p.write_text(s)
