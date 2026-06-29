<!-- Source: source/abd-bounded-context-map/stuff.docx | file:///C:/dev/abd-answers/source/abd-bounded-context-map/stuff.docx -->

“sufficient network bandwidth”. Technical tests are often written to verify non-functional requirements.

### Integration and Reuse

Mark the boundaries and relationships between different models and/or systems in a specific project, program, or organization to determine appropriate integration strategies and identify components for sharing or reuse. This is achieved by defining a Bounded Context clearly illustrating the applicability of each model. A specific bounded context may span an entire system, a portion of a system, or across several systems within the enterprise. Once bounded contexts have been defined, a Context Map is created that gives a global overview of the relevant model/system contexts and the relationships between them. Once a Context is Bounded, meaning that all elements within the context will make use of the same model elements, Continuous Integration is used to keep the model unified. This will ensure that the project will not disrupt other projects or systems that share the same objects.

#### Model Boundaries (Bounded Contexts)

Multiple models coexist on big projects and each model applies in a context. The context of a particular model may be a certain part of the code, or the work of a particular team. The model context is whatever set of conditions must apply in order to be able to say that the terms in a model have a specific meaning. In order to establish model boundaries or a bounded context, the context within which the model applies must be explicitly defined. This can be achieved through activities such as a brainstorming session. Once the context is defined, explicitly set boundaries in terms of team organization, usage within specific parts of the application, and physical manifestations such as code bases and database schemas. Keep the model strictly consistent within these bounds and ensure that it is well documented and understood.

Example: Booking Context

*A shipping company has an internal project to develop a new application for booking cargo. This application is to be driven by a domain specification. What is the bounded context within which this model applies? To answer this question, we have to look at what is happening on the project. This is a look at the project as it is, not as it ideally should be.*

*One project team is working on the booking application itself. They are not expected to modify the model objects, but the application they are building has to display and manipulate those objects. This team is a consumer of the model. The model is valid within the application (its primary consumer), and therefore the booking application is in bounds.*

*The completed bookings have to be passed to the legacy cargo-tracking system. A decision was made up front that the new model would depart from that of the legacy, so the legacy cargo-tracking system is outside the boundary. Necessary translation between the new model and the legacy is to be the responsibility of the legacy maintenance team. The translation mechanism is not driven by the model. It is not in the bounded context but is a part of the boundary itself. It is good that translation is out of context and not based on the model. It would be unrealistic to ask the legacy team to make any real use of the model because their primary work is out of context.*

*The team responsible for the model deals with the whole life cycle of each object, including persistence. Because this team has control of the database schema, they’ve been deliberately keeping the object-relational mapping straightforward. In other words, the schema is being driven by the model and therefore is in bounds.*

*Yet another team is working on a model and application for scheduling the voyages of the cargo ships. The scheduling and booking teams were initiated together, and both teams had intended to produce a single, unified system. The two teams have casually coordinated with each other, and they occasionally share objects, but they are not systematic about it. They are not working in the same bounded context. This is a risk, because they do not think of themselves as working on separate models. To the extent that they integrate, there will be problems unless they put in place processes to manage the situation. The first step, though, is to recognize the situation as it is. They are not in the same context and should stop trying to share code until some changes are made.*

*This bounded context is made up of all those aspects of the system that are driven by this particular model: the model objects, the database schema that persists the model objects, and the booking application. Two teams work primarily in this context: the modeling team and the application team. Information has to be exchanged with the legacy tracking system, and the legacy team has primary responsibility for the translation at this boundary, with cooperation from the modeling team. There is no clearly defined relationship between the booking model and the voyage schedule model, and defining that relationship should be one of the teams’ first actions. In the meantime, they should be very careful about sharing code or data.*

*So, what has been gained by defining this bounded context? For the teams working in context: clarity. Those two teams know they must stay consistent with one model. They make design decisions in that knowledge and watch for fractures. For the teams outside: freedom. They don’t have to walk in the gray zone, not using the same model, yet somehow feeling they should. But the most concrete gain in this particular case is probably realizing the risk of the informal sharing between the booking model team and the voyage schedule team. To avoid problems, they really need to decide on the cost/benefit trade-offs of sharing and put in processes to make it work. This won’t happen unless everyone understands where the bounds of the model contexts are.*

In defining model contexts, elements of distinct models are sometimes combined. Combining elements of distinct models causes two categories of problems:

* + **Duplicate Concepts** mean that there are two model elements (and attendant implementations) that actually represent the same concept. Every time this information changes, it has to be updated in two places with conversions. On top of that, the team members must learn not one but two ways of doing the same thing, along with all the ways they are being synchronized.
  + **False Cognates** may be slightly less common, but more harmful. This is the case when two people who are using the same term (or implemented object) think they are talking about the same thing, but really are not. Conflicts can be subtle when the two definitions are actually related to the same aspect in the domain, but have been conceptualized in slightly different ways. False cognates lead to development teams that step on each other’s code, databases that have weird contradictions, and confusion in the communication within the team.

If these problems are detected, a decision will need to be made on whether to pull the model back together to prevent fragmentation or let the groups develop independently.

#### Continuous Integration Strategy

When a number of people are working in the same bounded context, there is a strong tendency for the model to fragment. It is very hard to maintain the level of communication needed to develop a unified system of any size. Methods are needed to increase communication and reduce complexity. Continuous integration means that all work within the context is being merged and made consistent frequently enough that when splinters happen they are caught and corrected quickly. Continuous integration operates at two levels: Integration of model concepts via constant communication among team members and Integration of the implementation through implementation artifacts that are integrated by a systematic merge/build/test process that exposes issues early. Many processes for integration are used, but most of the effective ones share these characteristics:

* + A step-by-step, reproducible merge/build technique;
  + Automated test suites; and
  + Rules that set some reasonably small upper limit on the lifetime of unintegrated changes.

Continuous integration is essential only within a bounded context and should be applied within any individual bounded context that is larger than a two-person task.

Important:

Institute a process of merging all implementation artifacts frequently, with automated tests to flag fragmentation quickly. Continuously ensure that a shared view of the model is understood by all parties as the model concepts evolve. For more information on continuous integration see the following sites:

#### Relationships Between Bounded Contexts

An individual bounded context still does not provide a global view. The context of other models may still be vague and in flux. People on other teams won’t be very aware of the context bounds and will unknowingly make changes that blur the edges or complicate the interconnections. Confusion can be reduced by defining the relationship between the different contexts and creating a global view of all the model contexts on the project. Relationships can be defined using a context map. To create a context map follow these steps:

1. Identify each model in play on the project and define its bounded context
2. Name each bounded context and include the names in the Domain Language of the business domain model
3. Describe the points of contact between the models, outlining explicit translation for any communication

Example:

![](data:image/x-wmf;base64...)

![](data:image/x-wmf;base64...)

The relationships between bounded contexts take many forms depending on both design issues and project organizational issues. The following patterns cover a range of strategies for relating two models that can be composed to encompass an entire enterprise:

* **Shared kernel:** When functional integration is limited, the overhead of continuous integration may be too high. Separate bounded contexts may be defined and multiple teams formed. In this case, designate some subset of the domain model that the two teams agree to share. This includes, along with this subset of the model, the subset of code or of the database design associated with that part of the model. The shared subset should not be changed without consultation with the other team.

Diagram:

![](data:image/x-wmf;base64...)

* **Customer/supplier development teams:** Often one subsystem essentially feeds another and all the dependencies go one way. In this case, establish a clear customer/supplier relationship between the two teams. Make the dependant team play the customer role to the team it relies on. Negotiate and budget tasks for dependant team requirements so that everyone understands the commitment and schedule. Jointly develop automated acceptance tests that will validate the interface expected. Ensure that both teams use these tests as part of their own continuous integration.
* **Conformist:** The customer/supplier development teams pattern will not work in certain situations such as when the two teams are in different companies or very far apart in the management hierarchy. In the case where the model style for both teams is of good quality and reasonably comparable it may be best to give up on an independent model altogether. In this situation, the dependant team adheres to the model of the team upon which they depend. This may not yield the ideal model for the application but greatly simplifies integration. The conformist pattern is often appropriate when delivering an enterprise package solution (e.g. PeopleSoft, SAP) that requires a slight or moderate customization/configuration.
* **Anticorruption layer:** When a new system is being built that must have a large interface with another, the difficulty of relating the two models can eventually overwhelm the intent of the new model altogether, causing it to be modified to resemble the other system’s model, in an ad hoc fashion. In this case, create an isolation layer to provide clients with functionality in terms of their own domain model. The layer talks to the other system through its existing interface, requiring little or no modification to the other system. Internally, the layer translates in both directions as necessary between the two models.

Diagram:

![](data:image/x-wmf;base64...)

* **Separate ways:** Integration is always expensive and sometimes the benefits are small. In many circumstances, integration provides no significant benefit and may not be necessary. In this case, declare a bounded context to have no connection to the others at all, allowing developers to find simple, specialized solutions within this small scope.
* **Open host services:** When a subsystem has to be integrated with many others, customizing a translator for each can bog down the team. In this case, define a protocol that gives access to the subsystem as a set of services. Open the protocol so that all who need to integrate with the subsystem can use it. Enhance and expand the protocol to handle new requirements as necessary.
* **Published language:** Direct translation to and from the existing domain models may not be a good solution. Those models may be overly complex or poorly factored. In this case, use a well documented shared language that can express the necessary domain information as a common medium of communication, translating as necessary into and out of that language.

Diagram: Relative demands of each pattern

![](data:image/x-wmf;base64...)

In order to choose the right relationship, it is important to draw the context map to reflect the current situation at any given time. Once the context map is created it is possible to further define context boundaries and relationships. Some things to consider when choosing boundaries and relationships are:

* **Larger versus smaller:** There are benefits to employing a few larger bounded contexts or more smaller bounded contexts. Larger bounded contexts can help the flow between user tasks become smoother, make the model more coherent, and foster more communication. Smaller bounded contexts can reduce communication overhead, keep the model less abstract, and can be catered to special needs. Choosing the appropriate size for bounded contexts based on the situation.
* **Relationships with external systems:** When dealing with external systems, three of the above mentioned patterns apply: Separate ways, Conformist and Anticorruption Layer. If integration is not required then choosing to go Separate ways is the best option. If integration is required, then depending on the situation choose the Conformist, Anticorruption Layer, Open Host Services or Published Language patterns based on the situation.
* **Relationships within one system:** As a team grows larger, continuous integration can become more difficult. Make sure to recognize new developments within the system under design and implement patterns accordingly. For example, creating a shared kernel or setting up a customer/supplier development team relationship. Another example would be to let two models go their separate ways if it has been determined that they clash. A good rule of thumb is to limit a bounded context around teams of no greater then 10 people.
* **Transforming relationships:** There will be cases where the initial decisions about the boundaries and relationships between bounded contexts will change. Merging or changing the relationships between bounded contexts can be difficult. When conducting such changes, ensure that the current situation is fully understood, the end result is clearly defined and there are processes in place to execute the transformation.

Example: Digital Cargo File

The context map below depicts the situation in the Digital Cargo File project, with the project responsibilities on the right hand side of the figure.

Context map – Digital Cargo File

![](data:image/x-emf;base64...)

**The Model Contexts**

On the left side of the context map we find three existing contexts: Supply Operation - supporting delivery of cargo, Invoice and Trading - supporting sales of cargos. These three contexts exist inside different legacy systems that must be integrated with Digital Cargo File.

In the middle we find the Communication Gateway, enabling the business to send and receive email, fax and telex. The end-user is represented to illustrate the fact that humans must operate the communication gateway directly for the purpose of manual sending and filing of business messages, and filing of inbound messages from counterparties. This operation is known as document control.

On the right side we find the Digital Cargo File (DCF) with its three distinct model contexts: Front Page providing the cover page of a physical folder – used for content follow-up and case management, Folder providing the logical storage model and Document Storage defining the physical document storage model.

At the bottom we find Shipment & Allocation supporting oil field operation and owner allocation of produced volumes to be deployed for production in 2006.

**Context Map Analysis**

With the context map in place it is time for analysis. As stated earlier, the project team faced a set of problems that was hard to understand because the team was overwhelmed with details.

From the analysis of the context map it became clear that most of the encountered problems were caused by two factors:

• The role of the communication gateway

• The role of the front page

The actual problems will be described in the subsequent sections.

**The Role of the Communication Gateway**

The communication gateway had been operational for years when the digitized archive was envisioned. Inbound and outbound messages was printed and filed into the correct cargo folder whose front page was updated to reflect the changed state of the folder. As a curiosity its worth mentioning that the folder filled the role as relay stick used to pass the “case” from cargo operation to deal handling. Users found needed folders by inspecting each others desk.

In addition to support transmission of messages, the communication gateway was responsible for tracking when a message had been sent. This was known as document control. Users interacted directly with the communication system. It was assumed that the introduction of a digitized archive should support the same work practice.

When the project started to integrate with the communication gateway it was overwhelmed by problems such as:

* The need to replicate filing information into the communication gateway for the purpose of filing.
* The need to extend the communication gateway with additional user interfaces for the purpose of filing manually sent and received messages into the archive.
* Complex interface and information flows between front-end systems (Trading, Operation), the communication gateway and the DCF.

In the context map most of these problems materializes as complex dependencies between contexts.

**The Role of the Front Page**

In the paper based cargo file system the front page represented the key tool for follow-up of the actual folder (case). The front page contained aggregated cargo and deal information originating from the Supply Operation and Trading contexts respectively, combined with relevant information about the communication with the actual counterparties.

In the paper based world front page content, combined with who had the actual cargo file on their desktop, provided the required workflow support. Removing the physical folder required that DCF provided similar workflow support capabilities.

The project decided to provide the required capabilities by implementing the front page concept as an integral part of the archive. The front page was updated automatically by Trading and Supply Operation. Further the front page was extended with annotations to allow the users to use the front page as a scratchpad. The situation was further complicated as each business unit had their own variant of the front page but the project managed to convince the users to standardize on a limited number of variants.

After deployment the business have requested more advanced case management and workflow capabilities. These requests indicate that the attempted implementation of the paper based front page concept did not provide the required capabilities.

**Synthesis**

With the context map in our hands, analysis of encountered problems turned out to be easier as the cause of problems became visible. They where directly related to unhealthy structures in our architecture:

* Having the communication gateway as a spider in the web became counterproductive when moving from a paper based archive to a digital archive. The different links to the communication gateway represents only the top of the iceberg. Making a fax machine the core of a multi million IT system does not sound right.
* Extending the archive with case management capabilities polluted the archive with functionality not related to its prime objective: filing and retrieval of documents.

Based on analysis of the current situation a new context map reflecting a to-be picture was established and used to scope projects whose objective is to change the architecture.

**Recommended changes**

As stated in the previous section a new context map reflecting how we wanted our architecture to look like was developed. The key changes are:

* Front page concept moved out of the archive and extended to provide tailored workflow and case management capabilities.
* Document control moved from the Communication Gateway to the Folder context. The old folder context is renamed to Folder and Document Control.
* Front end systems interact with the Folder context through a service interface.

The actual changes are illustrated in below and described in more detail in the subsequent sections.

Updated Context map – Digital Cargo File

![](data:image/x-emf;base64...)

**Front page and case management**

As the physical front page was tightly coupled with deal and cargo information originating from Trading and Supply Operation respectively the Front Page context is moved out of the archive and closer to the Supply Operation and Trading.

The relationship between Front Page and Supply Operation / Trading is through use of an anticorruption layer. The rationale for using an anticorruption layer is the need to isolate the Front Page from Trading and Supply Operation.

The Front Page interacts with Folder and Document Control through the filing and communications service. This ensures loose coupling and facilitates a more service oriented architecture.

The main benefits from the separation of the Front Page from the Folder and Document Control are that a separated context is autonomous and as such simplifies tailoring without disruption of neighboring contexts.

**Document Control**

Document control is the name of the capability enabling users to file inbound messages into the archive. Due to historical reasons document control was part of the responsibility of the Communication Gateway. By moving document control from Communication Gateway and merge it with the Folder context two important improvements can be achieved:

* Users do not need to interact with the Communication Gateway improving their operational efficiency. Average time used to file an inbound message is estimated to be reduced with 30 seconds / message. With 1000 messages a day, that’s a significant improvement.
* Front end systems (Trading, Invoice, etc) do not need to interact with both the communication gateway and the folder contexts, reducing the number of couplings with 2/3 compared with the existing situation.

The impacts of these changes are clearly visible in the Updated Context Map.

**Filing and Communications Service**

Domain-Driven design advocates a principle called intention revealing interfaces. In a context map such intention revealing service is expressed as an “open host service”.

The project decided to introduce an “open host service” as access point to the Folder and Document Control context. The benefit from an “open-host-service” is that the service interface is documented and published as a first order design artifact that facilitates reuse.

The “open host service” pattern is also in line with the principles of service oriented architecture (SOA).

### Reference Architecture

Optionally, reference architecture may also be leveraged to reuse existing high-level architectures as a baseline that has solved similar problems in the past. Typically this is available in well-known domains with proven technologies that provide an integrated solution to solve a class of common problems. For example, reference architecture for Web 2.0 applications would be a proven reusable baseline that is optimized to support high volumes of traffic with primarily reads, real-time data integrity is not critical and needs to be cheap and horizontally scalable.

Sample Reference Architecture for a Web 2.0 Mobile Architecture:

![Mobile architecture.png](data:image/png;base64...)